import pandas as pd
from pathlib import Path

# =========================
# Paths
# =========================
BASE_DIR = Path(__file__).resolve().parents[1]

RAW_DATA_PATH = BASE_DIR / "data" / "raw" / "raw.csv"
PROCESSED_DATA_PATH = BASE_DIR / "data" / "processed" / "final.csv"


# =========================
# Step 1: Load data
# =========================
def load_data():
    print("Loading raw data...")
    df = pd.read_csv(RAW_DATA_PATH)
    return df


# =========================
# Step 2: Normalize columns
# =========================
def normalize_columns(df):
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace(r"[^\w]", "", regex=True)
    )
    return df
# datatype  correction 

def fix_dtypes(df):
    categorical_cols = [
        "gender",
        "drug_name"
    ]

    for col in categorical_cols:
        if col in df.columns:
            df[col] = df[col].astype("category")

    return df


# =========================
# Step 3: Handle missing values
# =========================
def handle_missing(df):
    print("Handling missing values...")

    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
    categorical_cols = df.select_dtypes(include=["object"]).columns

    for col in numeric_cols:
        df[col].fillna(df[col].median(), inplace=True)

    for col in categorical_cols:
        df[col].fillna(df[col].mode()[0], inplace=True)

    return df


# =========================
# Step 4: Remove duplicates
# =========================
def remove_duplicates(df):
    print("Removing duplicates...")
    return df.drop_duplicates()


# =========================
# Step 5: Handle outliers (IQR)
# =========================
def remove_outliers(df):
    print("Removing outliers using IQR...")
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns

    Q1 = df[numeric_cols].quantile(0.25)
    Q3 = df[numeric_cols].quantile(0.75)
    IQR = Q3 - Q1

    df = df[~((df[numeric_cols] < (Q1 - 1.5 * IQR)) |
              (df[numeric_cols] > (Q3 + 1.5 * IQR))).any(axis=1)]

    return df


# =========================
# Main pipeline
# =========================
def run_pipeline():
    df = load_data()
    df = normalize_columns(df)
    df = fix_dtypes(df) 
    df = handle_missing(df)
    df = remove_duplicates(df)
    df = remove_outliers(df)

    PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_DATA_PATH, index=False)

    print("Pipeline completed.")
    print(f"Final data saved at: {PROCESSED_DATA_PATH}")


if __name__ == "__main__":
    run_pipeline()
