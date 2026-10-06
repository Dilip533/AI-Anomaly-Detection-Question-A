import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.metrics import precision_recall_fscore_support

SEED = int(input("Enter your USN seed: "))
df = pd.read_csv("../setup/readings.csv")
y = df["label"].to_numpy()
hr = df["hr"].to_numpy(float)
acc = df["acc"].to_numpy(float)

# Simple features for the unsupervised detector.
roll_mean = pd.Series(hr).rolling(60, min_periods=1).mean().to_numpy()
roll_std = pd.Series(hr).rolling(60, min_periods=1).std().fillna(0).to_numpy()
delta = np.abs(np.diff(hr, prepend=hr[0]))
X = np.column_stack([hr, acc, roll_mean, roll_std, delta])

print("\nLEVEL 1 - ISOLATION FOREST")
model = IsolationForest(n_estimators=200, contamination=0.03, random_state=SEED)
pred_if = (model.fit_predict(X) == -1).astype(int)
for kind in ["spike", "drop-out", "silent drift"]:
    actual = (df["anomaly_type"].to_numpy() == kind).astype(int)
    p, r, f, _ = precision_recall_fscore_support(actual, pred_if, average="binary", zero_division=0)
    print(f"{kind:13s} precision={p:.3f} recall={r:.3f} F1={f:.3f}")
walking = (acc > 0.45) & (y == 0)
print("False alarms during walking:", int(np.sum(pred_if[walking] == 1)))

# LEVEL 2 - written from scratch using NumPy for the detector and metrics.
def rolling_zscore(x, window=300, threshold=2.5):
    x = np.asarray(x, dtype=float)
    out = np.zeros(len(x), dtype=int)
    for i in range(window, len(x)):
        previous = x[i-window:i]
        mean = np.mean(previous)
        std = np.std(previous)
        z = 0 if std == 0 and x[i] == mean else (np.inf if std == 0 else abs((x[i]-mean)/std))
        if z > threshold:
            out[i] = 1
    return out

def scores(y_true, y_pred):
    tp = np.sum((y_true == 1) & (y_pred == 1))
    fp = np.sum((y_true == 0) & (y_pred == 1))
    fn = np.sum((y_true == 1) & (y_pred == 0))
    precision = tp/(tp+fp) if tp+fp else 0
    recall = tp/(tp+fn) if tp+fn else 0
    f1 = 2*precision*recall/(precision+recall) if precision+recall else 0
    return precision, recall, f1

pred_z = rolling_zscore(hr)
print("\nLEVEL 2 - ROLLING Z-SCORE")
p, r, f = scores(y, pred_z)
sp, sr, sf, _ = precision_recall_fscore_support(y, pred_z, average="binary", zero_division=0)
print(f"Overall (own):    precision={p:.3f} recall={r:.3f} F1={f:.3f}")
print(f"Overall (sklearn): precision={sp:.3f} recall={sr:.3f} F1={sf:.3f}")
for kind in ["spike", "drop-out", "silent drift"]:
    actual = (df["anomaly_type"].to_numpy() == kind).astype(int)
    p, r, f = scores(actual, pred_z)
    print(f"{kind:13s} precision={p:.3f} recall={r:.3f} F1={f:.3f}")
print("False alarms during walking:", int(np.sum(pred_z[walking] == 1)))

# LEVEL 3 prediction is written before the comparison below.
print("\nLEVEL 3 - PREDICTION")
print("Prediction: doubling the window from 300 s to 600 s will reduce silent-drift recall.")
print("Reason: the slow drift is compared with a longer history, so each change should look less unusual.")
pred_z_600 = rolling_zscore(hr, window=600, threshold=2.5)
silent = (df["anomaly_type"].to_numpy() == "silent drift").astype(int)
_, r300, _ = scores(silent, pred_z)
_, r600, _ = scores(silent, pred_z_600)
print(f"Silent-drift recall, 300 s: {r300:.3f}")
print(f"Silent-drift recall, 600 s: {r600:.3f}")
print("Prediction result:", "correct" if r600 < r300 else "not correct")

for name, pred in [("isolation_forest", pred_if), ("rolling_zscore", pred_z)]:
    missed = np.where((y == 1) & (pred == 0))[0]
    if len(missed):
        center = int(missed[0])
        lo, hi = max(0, center-60), min(len(df), center+61)
        plt.figure(figsize=(10,4))
        plt.plot(np.arange(lo,hi), hr[lo:hi])
        plt.axvline(center, linestyle="--")
        plt.xlabel("Reading number")
        plt.ylabel("Heart rate")
        plt.title(f"{name}: missed {df['anomaly_type'].iloc[center]}")
        plt.tight_layout()
        plt.savefig(f"{name}_missed.png", dpi=150)
        plt.close()
        print(f"{name} missed: {df['anomaly_type'].iloc[center]} at row {center}")
