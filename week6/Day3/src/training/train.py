import json
import joblib
import numpy as np
import pandas as pd
from pathlib import Path

from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    ConfusionMatrixDisplay
)
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier

# If XGBoost is installed
try:
    from xgboost import XGBClassifier
    XGB_AVAILABLE = True
except ImportError:
    XGB_AVAILABLE = False

import matplotlib.pyplot as plt

# --------------------------------------------------
# Paths
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[3]

DATA_DIR = BASE_DIR / "Day2" / "src" / "data" / "processed"
FEATURES_PATH = BASE_DIR / "Day2" / "src" / "features" / "feature_list.json"

MODELS_DIR = BASE_DIR / "Day3" / "models"
EVAL_DIR = BASE_DIR / "Day3" / "evaluation"

MODELS_DIR.mkdir(parents=True, exist_ok=True)
EVAL_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# Load data
# --------------------------------------------------
def load_data():
    X_train = pd.read_csv(DATA_DIR / "X_train.csv")
    X_test = pd.read_csv(DATA_DIR / "X_test.csv")
    y_train = pd.read_csv(DATA_DIR / "y_train.csv").squeeze()
    y_test = pd.read_csv(DATA_DIR / "y_test.csv").squeeze()

    with open(FEATURES_PATH, "r") as f:
        feature_list = list(json.load(f).values())

    return X_train[feature_list], X_test[feature_list], y_train, y_test


# --------------------------------------------------
# Define models
# --------------------------------------------------
def get_models():
    models = {
        "LogisticRegression": LogisticRegression(
            max_iter=2000,
            penalty="l2",
            solver="liblinear"
        ),
        "RandomForest": RandomForestClassifier(
            n_estimators=200,
            max_depth=8,
            random_state=42
        ),
        "NeuralNetwork": MLPClassifier(
            hidden_layer_sizes=(64, 32),
            max_iter=500,
            random_state=42
        )
    }

    if XGB_AVAILABLE:
        models["XGBoost"] = XGBClassifier(
            n_estimators=200,
            max_depth=4,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            eval_metric="logloss",
            random_state=42
        )

    return models


# --------------------------------------------------
# Cross-validation evaluation
# --------------------------------------------------
def evaluate_model(model, X, y):
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    scoring = {
        "accuracy": "accuracy",
        "precision": "precision",
        "recall": "recall",
        "f1": "f1",
        "roc_auc": "roc_auc"
    }

    scores = cross_validate(
        model,
        X,
        y,
        cv=cv,
        scoring=scoring,
        return_train_score=False
    )

    return {metric: scores[f"test_{metric}"].mean() for metric in scoring}


# --------------------------------------------------
# Train, compare, select best model
# --------------------------------------------------
def main():
    X_train, X_test, y_train, y_test = load_data()
    models = get_models()

    results = {}
    best_model = None
    best_score = -1

    print("\n🔹 Training models with 5-fold CV\n")

    for name, model in models.items():
        print(f"Training {name}...")
        metrics = evaluate_model(model, X_train, y_train)
        results[name] = metrics

        # Select best model using ROC-AUC
        if metrics["roc_auc"] > best_score:
            best_score = metrics["roc_auc"]
            best_model = model
            best_model_name = name

    print(f"\n✅ Best model: {best_model_name}")

    # --------------------------------------------------
    # Train best model on full training data
    # --------------------------------------------------
    best_model.fit(X_train, y_train)

    # Save model
    joblib.dump(best_model, MODELS_DIR / "best_model.pkl")

    # --------------------------------------------------
    # Final evaluation on test set
    # --------------------------------------------------
    y_pred = best_model.predict(X_test)
    y_prob = best_model.predict_proba(X_test)[:, 1]

    test_metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1": f1_score(y_test, y_pred),
        "roc_auc": roc_auc_score(y_test, y_prob)
    }

    results["BEST_MODEL_TEST"] = {
        "model": best_model_name,
        **test_metrics
    }

    # Save metrics
    with open(EVAL_DIR / "metrics.json", "w") as f:
        json.dump(results, f, indent=4)

    # --------------------------------------------------
    # Confusion matrix
    # --------------------------------------------------
    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(cm)
    disp.plot()
    plt.title(f"Confusion Matrix — {best_model_name}")
    plt.savefig(EVAL_DIR / "confusion_matrix.png")
    plt.close()

    print("\n Metrics saved to evaluation/metrics.json")
    print(" Best model saved to models/best_model.pkl")
    print(" Confusion matrix saved")

    print("\n DAY 3 COMPLETED SUCCESSFULLY")


if __name__ == "__main__":
    main()
