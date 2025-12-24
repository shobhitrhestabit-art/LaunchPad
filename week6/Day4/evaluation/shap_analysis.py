import json
import shap
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

# --------------------------------------------------
# Resolve project root robustly
# --------------------------------------------------
def get_project_root():
    path = Path(__file__).resolve()
    for parent in path.parents:
        if parent.name == "week6(practice)":
            return parent
    raise RuntimeError("Project root not found")

BASE_DIR = get_project_root()

DATA_DIR = BASE_DIR / "Day2" / "src" / "data" / "processed"
FEATURES_PATH = BASE_DIR / "Day2" / "src" / "features" / "feature_list.json"
MODEL_PATH = BASE_DIR / "Day3" / "models" / "best_model.pkl"

OUTPUT_DIR = BASE_DIR / "Day4" / "evaluation"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# Load data & model
# --------------------------------------------------
def load_assets():
    X = pd.read_csv(DATA_DIR / "X_train.csv")

    with open(FEATURES_PATH, "r") as f:
        features = list(json.load(f).values())

    X = X[features]

    model = joblib.load(MODEL_PATH)
    return X, model


# --------------------------------------------------
# SHAP analysis
# --------------------------------------------------
def run_shap():
    X, model = load_assets()
    print("🔍 Computing SHAP values...")

    # -----------------------------
    # Choose correct SHAP explainer
    # -----------------------------
    if hasattr(model, "coef_"):
        # Linear models (Logistic Regression)
        masker = shap.maskers.Independent(X)
        explainer = shap.LinearExplainer(model, masker)
        shap_values = explainer.shap_values(X)
    else:
        # Tree-based models
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X)

    # For binary classification
    if isinstance(shap_values, list):
        shap_values = shap_values[1]

    # --------------------------------------------------
    # SHAP summary plot
    # --------------------------------------------------
    plt.figure()
    shap.summary_plot(
        shap_values,
        X,
        show=False
    )
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "shap_summary.png")
    plt.close()

    # --------------------------------------------------
    # Feature importance (mean |SHAP|)
    # --------------------------------------------------
    importance = np.abs(shap_values).mean(axis=0)
    importance_df = pd.DataFrame({
        "feature": X.columns,
        "importance": importance
    }).sort_values(by="importance", ascending=False)

    plt.figure(figsize=(8, 6))
    plt.barh(
        importance_df["feature"],
        importance_df["importance"]
    )
    plt.gca().invert_yaxis()
    plt.title("Feature Importance (SHAP)")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "feature_importance.png")
    plt.close()

    print("SHAP analysis completed")
    print("Saved shap_summary.png and feature_importance.png")


if __name__ == "__main__":
    run_shap()
