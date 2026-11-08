import joblib
import pandas as pd

from pathlib import Path
from sqlalchemy.orm import Session

from backend.services.feature_service import extract_customer_features


# =====================================================
# Load Random Forest Model
# =====================================================

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = BASE_DIR / "ml_training" / "random_forest_model.pkl"

model = joblib.load(MODEL_PATH)


# =====================================================
# Credit Risk Prediction
# =====================================================

def predict_credit_risk(db: Session, national_id: str):

    # 1. Extract customer features from Database
    features = extract_customer_features(
        db=db,
        national_id=national_id
    )

    # 2. Convert features to DataFrame
    customer_df = pd.DataFrame([features])

    # 3. Random Forest Prediction
    prediction = model.predict(customer_df)[0]

    # 4. Find Default class probability (class 1)
    classes = list(model.classes_)
    default_index = classes.index(1)

    probability = model.predict_proba(customer_df)[0][default_index]

    # 5. Calculate Risk Score
    risk_score = probability * 100

    return {
        "prediction": int(prediction),
        "default_probability": round(float(probability), 4),
        "risk_score": round(float(risk_score), 2)
    }