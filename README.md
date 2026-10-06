# AI-Driven Anomaly Detection and Monitoring System

Questions completed: **A and C**

Personal seed S: **2506** (last four digits of USN)

## Run order

### 1. Generate the personal dataset

From the repository root:

    cd setup
    python generate_data.py

Enter `2506` when asked.

This creates `readings.csv` and `full_signal.png`.

### 2. Run Question A

    cd ../question_A
    python detect.py

Enter `2506` when asked.

This runs Levels 1, 2 and 3 and creates the two missed-anomaly plots.

### 3. Run Question C

    cd ../question_C
    python run_sql.py

This creates/updates `monitoring.db` and prints the three required SQL query outputs.

The Level 3 scaling calculation is documented in `level3/scaling.md`.

## Libraries

Python, NumPy, Pandas, Matplotlib, scikit-learn and SQLite.

## Personal intelligence / AI use

See `PERSONAL_INTELLIGENCE.md`. The final numbers were produced by running the code with seed 2506.