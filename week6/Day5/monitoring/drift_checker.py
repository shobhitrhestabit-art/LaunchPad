import pandas as pd
import numpy as np
from pathlib import Path
from scipy.stats import ks_2samp
import json


def get_project_root():
    path = Path(__file__).resolve()
    for parent in path.parents:
        if parent.name == "week6(practice)":
            return parent
    raise RuntimeError("Project root not found")

BASE_DIR = get_project_root()


TRAIN_DATA_PATH = BASE_DIR / "Day2" / "src" / "data" / "processed" / "X_train.csv"
PREDICTION_LOG_PATH = BASE_DIR / "Day5" / "prediction_logs.csv"
OUTPUT_PATH = BASE_DIR / "Day5" / "monitoring" / "drift_report.json"


DRIFT_THRESHOLD_PVALUE = 0.05  


def load_data():
    train_df = pd.read_csv(TRAIN_DATA_PATH)
    live_df = pd.read_csv(PREDICTION_LOG_PATH)

    
    drop_cols = ["request_id", "timestamp", "prediction", "probability", "model_version"]
    live_df = live_df.drop(columns=[c for c in drop_cols if c in live_df.columns])

    #
    common_cols = train_df.columns.intersection(live_df.columns)

    return train_df[common_cols], live_df[common_cols]


def detect_drift(train_df, live_df):
    drift_results = {}

    for col in train_df.columns:
        train_values = train_df[col].dropna()
        live_values = live_df[col].dropna()

        
        if len(live_values) < 20:
            drift_results[col] = {
                "status": "insufficient_data"
            }
            continue

        stat, p_value = ks_2samp(train_values, live_values)

        drift_results[col] = {
            "p_value": round(float(p_value), 6),
            "drift_detected": bool(p_value < DRIFT_THRESHOLD_PVALUE)
        }

    return drift_results


def main():
    print("🔍 Running data drift detection...")

    train_df, live_df = load_data()

    drift_results = detect_drift(train_df, live_df)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(drift_results, f, indent=2)

    drifted = [
        f for f, r in drift_results.items()
        if r.get("drift_detected") is True
    ]

    print(" Drift check completed")
    print(f" Drifted features: {drifted if drifted else 'None'}")
    print(f" Report saved to: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
