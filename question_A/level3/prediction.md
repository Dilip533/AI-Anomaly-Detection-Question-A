# Level 3 prediction

Prediction made before the comparison:

If the rolling window is doubled from 300 seconds to 600 seconds, silent-drift recall will decrease.

Reason: silent drift is a slow 15 bpm increase over five minutes. With a longer history, the current value is compared with a wider normal period, so the change should look less unusual.

Result with seed 2506:
- 300-second window recall: 0.014
- 600-second window recall: 0.000

The prediction was correct.
