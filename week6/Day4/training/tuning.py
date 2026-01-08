import json
import optuna
import joblib
import numpy as np
import pandas as pd
from pathlib import Path

from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score


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
RESULTS_PATH = BASE_DIR / "Day4" / "tuning" / "results.json"

RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)


def load_data():
    X = pd.read_csv(DATA_DIR / "X_train.csv")
    y = pd.read_csv(DATA_DIR / "y_train.csv").squeeze()

    with open(FEATURES_PATH, "r") as f:
        features = list(json.load(f).values())

    return X[features], y



def objective(trial):
    params = {
        "n_estimators": trial.suggest_int("n_estimators", 100, 500),
        "max_depth": trial.suggest_int("max_depth", 3, 12),
        "min_samples_split": trial.suggest_int("min_samples_split", 2, 10),
        "min_samples_leaf": trial.suggest_int("min_samples_leaf", 1, 5),
        "max_features": trial.suggest_categorical(
            "max_features", ["sqrt", "log2"]
        ),
        "random_state": 42,
        "n_jobs": -1
    }

    model = RandomForestClassifier(**params)

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    scores = cross_val_score(
        model,
        X_train,
        y_train,
        cv=cv,
        scoring="roc_auc"
    )

    return scores.mean()


def main():
    global X_train, y_train
    X_train, y_train = load_data()

    print("🔍 Starting hyperparameter tuning with Optuna...\n")

    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=30)

    print("Tuning completed")

    best_params = study.best_params
    best_score = study.best_value


    baseline_model = joblib.load(MODEL_PATH)

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    baseline_scores = cross_val_score(
        baseline_model,
        X_train,
        y_train,
        cv=cv,
        scoring="roc_auc"
    )

    baseline_score = baseline_scores.mean()


    results = {
        "baseline_roc_auc": baseline_score,
        "tuned_roc_auc": best_score,
        "improvement": best_score - baseline_score,
        "best_hyperparameters": best_params
    }

    with open(RESULTS_PATH, "w") as f:
        json.dump(results, f, indent=4)

    print("\n Baseline ROC-AUC:", round(baseline_score, 4))
    print(" Tuned ROC-AUC:", round(best_score, 4))
    print(" Improvement:", round(best_score - baseline_score, 4))

    print("\n Results saved to Day4/tuning/results.json")


if __name__ == "__main__":
    main()
