# Level 2 - Rolling z-score

The rolling z-score detector and the precision/recall/F1 function are written directly with NumPy in `../level1_and_2_and_3.py`.

No pandas rolling operation or scikit-learn is used for the detector itself. Scikit-learn is used only afterward to verify that the manually calculated overall metrics match.
