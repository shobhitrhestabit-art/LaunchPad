import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parents[3]

DATA_PATH = BASE_DIR / "Day1" / "src" / "data" / "processed" / "final.csv"
OUTPUT_DIR = BASE_DIR / "Day2" / "src" / "data" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TARGET = "nephrotoxic_label"


def load_data():
    return pd.read_csv(DATA_PATH)


def encode_categorical(df):
    return pd.get_dummies(
        df,
        columns=["gender", "drug_name"],
        drop_first=True
    )


def generate_features(df):
    eps = 1e-6  # small constant to avoid division by zero

    # ---- Clinical ratios ----
    df["bp_ratio"] = df["bp_systolic"] / (df["bp_diastolic"] + eps)
    df["creatinine_urea_ratio"] = df["serum_creatinine"] / (df["blood_urea"] + eps)

    # ---- Drug exposure features ----
    df["drug_exposure_intensity"] = df["drug_dosage_mg"] * df["exposure_days"]
    df["binding_adjusted_dose"] = (
        df["drug_dosage_mg"] * (1 - df["protein_binding_pct"] / 100)
    )

    # ---- Toxicity aggregation ----
    df["toxicity_load"] = df["mitochondrial_damage"] + df["oxidative_stress"]

    # ---- Pharmacokinetic features ----
    df["pk_risk_score"] = df["half_life_hr"] / (df["clearance_rate"] + eps)
    df["bioavailability_clearance_ratio"] = (
        df["bioavailability_pct"] / (df["clearance_rate"] + eps)
    )

    # ---- Kidney stress indicators ----
    df["renal_stress_index"] = (
        df["serum_creatinine_change_pct"] +
        df["kidney_cell_viability_pct"]
    )

    return df


def split_and_scale(df):
    X = df.drop(columns=[TARGET, "ckd_risk_label"])

    y = df[TARGET]

    # Convert everything to float (critical step)
    X = X.astype(float)

    # Replace invalid values
    X = X.replace([np.inf, -np.inf], np.nan)
    X = X.fillna(0)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    X_train_scaled = pd.DataFrame(
        X_train_scaled, columns=X_train.columns
    )
    X_test_scaled = pd.DataFrame(
        X_test_scaled, columns=X_test.columns
    )

    return X_train_scaled, X_test_scaled, y_train, y_test


def save_outputs(X_train, X_test, y_train, y_test):
    X_train.to_csv(OUTPUT_DIR / "X_train.csv", index=False)
    X_test.to_csv(OUTPUT_DIR / "X_test.csv", index=False)
    y_train.to_csv(OUTPUT_DIR / "y_train.csv", index=False)
    y_test.to_csv(OUTPUT_DIR / "y_test.csv", index=False)


def main():
    df = load_data()
    df = encode_categorical(df)
    df = generate_features(df)

    X_train, X_test, y_train, y_test = split_and_scale(df)
    save_outputs(X_train, X_test, y_train, y_test)

    print(" build_features.py completed successfully")


if __name__ == "__main__":
    main()
