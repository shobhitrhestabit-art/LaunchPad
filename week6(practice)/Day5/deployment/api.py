import uuid
import json
import joblib
import pandas as pd
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# --------------------------------------------------
# Resolve project root robustly
# --------------------------------------------------


# --------------------------------------------------
# Resolve project root (Docker-safe)
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[2]



# --------------------------------------------------
# Paths & config
# --------------------------------------------------
MODEL_PATH = BASE_DIR / "Day3" / "models" / "best_model.pkl"
FEATURES_PATH = BASE_DIR / "Day2" / "src" / "features" / "feature_list.json"
LOG_PATH = BASE_DIR / "Day5" / "prediction_logs.csv"

MODEL_VERSION = "v1.0"

# --------------------------------------------------
# Load model & feature list (once at startup)
# --------------------------------------------------
try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    raise RuntimeError(f"Failed to load model: {e}")

with open(FEATURES_PATH, "r") as f:
    FEATURE_NAMES = list(json.load(f).values())

# --------------------------------------------------
# FastAPI app
# --------------------------------------------------
app = FastAPI(
    title="Nephrotoxicity Risk Prediction API",
    description="Predicts drug-induced nephrotoxicity risk",
    version=MODEL_VERSION
)

# --------------------------------------------------
# Input schema
# --------------------------------------------------
class PredictionRequest(BaseModel):
    features: dict = Field(
        ...,
        description="Dictionary of feature_name: value"
    )

# --------------------------------------------------
# Utility: log prediction
# --------------------------------------------------
def log_prediction(row: dict):
    df = pd.DataFrame([row])
    if LOG_PATH.exists():
        df.to_csv(LOG_PATH, mode="a", header=False, index=False)
    else:
        df.to_csv(LOG_PATH, index=False)

# --------------------------------------------------
# Prediction endpoint
# --------------------------------------------------
@app.post("/predict")
def predict(request: PredictionRequest):
    request_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat()

    # -----------------------------
    # Input validation
    # -----------------------------
    incoming_features = request.features

    missing_features = set(FEATURE_NAMES) - set(incoming_features.keys())
    if missing_features:
        raise HTTPException(
            status_code=400,
            detail=f"Missing features: {list(missing_features)}"
        )

    # -----------------------------
    # Prepare input
    # -----------------------------
    try:
        X = pd.DataFrame([incoming_features])[FEATURE_NAMES]
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid input format: {e}"
        )

    # -----------------------------
    # Model inference
    # -----------------------------
    try:
        probability = float(model.predict_proba(X)[0][1])
        prediction = int(probability >= 0.5)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {e}"
        )

    # -----------------------------
    # Logging
    # -----------------------------
    log_row = {
        "request_id": request_id,
        "timestamp": timestamp,
        "prediction": prediction,
        "probability": probability,
        "model_version": MODEL_VERSION,
        **incoming_features
    }
    log_prediction(log_row)

    # -----------------------------
    # Response
    # -----------------------------
    return {
        "request_id": request_id,
        "prediction": prediction,
        "risk_probability": round(probability, 4),
        "model_version": MODEL_VERSION
    }

# --------------------------------------------------
# Health check
# --------------------------------------------------
@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_version": MODEL_VERSION
    }
