import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.feature_selection import mutual_info_classif, RFE
from sklearn.linear_model import LogisticRegression


# -----------------------------
# Resolve project root safely
# -----------------------------
BASE_DIR = Path(__file__).resolve().parents[3]

DATA_DIR = BASE_DIR / "Day2" / "src" / "data" / "processed"
FEATURES_DIR = BASE_DIR / "Day2" / "src" / "features"


def load_data():
    X_train = pd.read_csv(DATA_DIR / "X_train.csv")
    y_train = pd.read_csv(DATA_DIR / "y_train.csv").squeeze()
    return X_train, y_train




def correlation_filter(X, threshold=0.9):
    corr = X.corr().abs()

    upper = corr.where(
        np.triu(np.ones(corr.shape), k=1).astype(bool)
    )

    drop_cols = [
        col for col in upper.columns if any(upper[col] > threshold)
    ]

    return X.drop(columns=drop_cols), drop_cols


def mutual_information_filter(X, y, top_k=20):
    mi = mutual_info_classif(X, y)
    mi_scores = pd.Series(mi, index=X.columns).sort_values(ascending=False)
    return mi_scores.head(top_k), mi_scores


def rfe_filter(X, y, n_features=15):
    model = LogisticRegression(max_iter=2000)
    rfe = RFE(model, n_features_to_select=n_features)
    rfe.fit(X, y)
    return X.columns[rfe.support_].tolist()


def main():
    X, y = load_data()

    # Step 1: Correlation filtering
    X_corr, dropped = correlation_filter(X)

    # Step 2: Mutual Information
    top_mi, mi_scores = mutual_information_filter(X_corr, y)

    # Step 3: RFE
    final_features = rfe_filter(X_corr[top_mi.index], y)

    FEATURES_DIR.mkdir(parents=True, exist_ok=True)

    pd.Series(final_features).to_json(
        FEATURES_DIR / "feature_list.json",
        indent=2
    )

    print("feature_selector.py completed successfully")
    print("Final selected features:")
    print(final_features)


if __name__ == "__main__":
    main()
