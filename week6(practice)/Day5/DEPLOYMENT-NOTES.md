# Day 5 — Model Deployment & Monitoring (Capstone)

## Overview
This project deploys a trained machine learning model to predict
drug-induced nephrotoxicity risk using a REST API.

The system follows a production-oriented design with logging,
monitoring, and drift detection.

---

## Model Summary
- Task: Binary classification
- Target: nephrotoxic_label
- Final Model: Logistic Regression
- Training: Cross-validation + hyperparameter tuning
- Explainability: SHAP-based analysis

---

## API Deployment
- Framework: FastAPI
- Endpoint: POST /predict
- Health check: GET /health
- Model loaded using joblib at startup

### Input
JSON payload containing feature-value pairs.

### Output
- prediction (0/1)
- risk_probability
- model_version
- request_id

---

## Prediction Logging
Each prediction request is logged to `prediction_logs.csv` with:
- request_id
- timestamp
- prediction
- probability
- model_version
- input features

This supports auditing, debugging, and retraining.

---

## Monitoring & Drift Detection
A drift detection script compares:
- Training data distributions
- Live inference data distributions

Method:
- Kolmogorov–Smirnov (KS) test
- Drift flagged when p-value < 0.05

This helps identify data shifts that may impact model performance.

---

## Deployment Readiness
- Container-ready using Docker
- Dependencies pinned via requirements.txt
- Environment variables documented
- Suitable for local or cloud deployment

---

## Conclusion
This capstone demonstrates an end-to-end ML system:
data → features → model → deployment → monitoring.

It reflects real-world MLOps practices and production awareness.
