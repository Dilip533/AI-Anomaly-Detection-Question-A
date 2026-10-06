import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

S = int(input("Enter the last four digits of your USN: "))
rng = np.random.default_rng(S)

N = 7200
t = np.arange(N)
timestamp = pd.date_range("2026-10-06 09:00:00", periods=N, freq="s")
rest = 60 + (S % 20)

hr = rest + 2*np.sin(2*np.pi*t/1800) + 1.5*np.sin(2*np.pi*t/25) + rng.normal(0, 1.2, N)
acc = np.abs(rng.normal(0.08, 0.035, N))

# Three normal walking periods. Walking is NOT an anomaly.
walking_periods = [(900, 1200), (3000, 3480), (5200, 5680)]
for start, end in walking_periods:
    acc[start:end] += rng.normal(0.85, 0.12, end-start)
    hr[start:end] += 24 + 2*np.sin(np.linspace(0, np.pi, end-start))

label = np.zeros(N, dtype=int)
anomaly_type = np.array(["normal"] * N, dtype=object)

# Select 20 non-overlapping events outside walking periods.
# 7 spikes, 7 drop-outs and 6 silent drifts = 20 events.
types = ["spike"]*7 + ["drop-out"]*7 + ["silent drift"]*6
rng.shuffle(types)
events = []
blocked = np.zeros(N, dtype=bool)
for s, e in walking_periods:
    blocked[max(0, s-20):min(N, e+20)] = True

for kind in types:
    length = 300 if kind == "silent drift" else (10 if kind == "spike" else 30)
    possible = np.where(~blocked)[0]
    possible = possible[(possible >= 30) & (possible < N-length-20)]
    possible = [int(x) for x in possible if not blocked[x:x+length+20].any()]
    if not possible:
        raise RuntimeError("Could not place all 20 non-overlapping anomalies")
    start = int(rng.choice(possible))
    events.append((start, kind))
    blocked[start:start+length+20] = True

events.sort(key=lambda x: x[0])

for start, kind in events:
    if kind == "spike":
        length = int(rng.integers(3, 11))
        hr[start:start+length] += rng.uniform(45, 60)
        label[start:start+length] = 1
        anomaly_type[start:start+length] = "spike"
    elif kind == "drop-out":
        length = int(rng.integers(10, 31))
        hr[start:start+length] = 0
        label[start:start+length] = 1
        anomaly_type[start:start+length] = "drop-out"
    else:
        length = 300
        hr[start:start+length] += np.linspace(0, 15, length)
        label[start:start+length] = 1
        anomaly_type[start:start+length] = "silent drift"

df = pd.DataFrame({
    "timestamp": timestamp,
    "hr": hr.round(3),
    "acc": acc.round(3),
    "label": label,
    "anomaly_type": anomaly_type
})
df.to_csv("readings.csv", index=False)

plt.figure(figsize=(14, 5))
plt.plot(df["hr"], linewidth=0.8, label="Heart rate")
for kind, marker in [("spike", "r"), ("drop-out", "g"), ("silent drift", "m")]:
    idx = np.where(df["anomaly_type"].to_numpy() == kind)[0]
    plt.scatter(idx, df.loc[idx, "hr"], s=8, label=kind)
plt.xlabel("Reading number")
plt.ylabel("Heart rate (bpm)")
plt.title(f"Wearable signal - seed {S}")
plt.legend()
plt.tight_layout()
plt.savefig("full_signal.png", dpi=150)
plt.close()

print("Created readings.csv:", len(df), "rows")
print("Anomaly events:", len(events))
print(df["anomaly_type"].value_counts())
print("Seed:", S)
