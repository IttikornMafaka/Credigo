import joblib
import pandas as pd

from pathlib import Path
from backend.schemas.prediction import CreditPredictionRequest


# =====================================================
# Load Random Forest Model
# =====================================================

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = BASE_DIR / "ml_training" / "random_forest_model.pkl"

model = joblib.load(MODEL_PATH)


# =====================================================
# Credit Risk Prediction
# =====================================================

def predict_credit_risk(customer_data: CreditPredictionRequest):

    # Convert Pydantic Schema to Dictionary
    customer_dict = customer_data.model_dump()

    # Convert Dictionary to DataFrame
    customer_df = pd.DataFrame([customer_dict])

    # Random Forest Prediction
    prediction = model.predict(customer_df)[0]

    # Default Probability
    probability = model.predict_proba(customer_df)[0][1]

    # Risk Score
    risk_score = probability * 100

    return {
        "prediction": int(prediction),
        "default_probability": round(float(probability), 4),
        "risk_score": round(float(risk_score), 2)
    }