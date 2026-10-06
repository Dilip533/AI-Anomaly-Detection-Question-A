# Missed anomaly explanation

The script saves one missed-anomaly plot for each method.

The rolling z-score method can miss an anomaly when the current value is not far enough from the mean of its previous window. A long, slow change can therefore look normal compared with the recent history.

Isolation Forest can miss an anomaly when its feature values are not isolated enough from other observations. In this run, a missed drop-out is used as the example.
