
import joblib
import pandas as pd

from pathlib import Path
from math import isfinite
from sqlalchemy.orm import Session

from backend.services.feature_service import extract_customer_features
from app.model.session import Customer, Predicthistory


# =====================================================
# Load Random Forest Model
# =====================================================

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = BASE_DIR / "ml_training" / "random_forest_model.pkl"

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Random Forest model not found: {MODEL_PATH}"
    )

model = joblib.load(MODEL_PATH)

MODEL_VERSION = "random_forest_v1"

DEFAULT_CLASS = 1


# =====================================================
# Credit Risk Prediction + History
# =====================================================

def predict_credit_risk(db: Session, national_id: str):

    try:

        # 1. Validate Input
        if not national_id:
            raise ValueError("National ID is required")

        # 2. Find Customer
        customer = (
            db.query(Customer)
            .filter(Customer.national_id == national_id)
            .first()
        )

        if customer is None:
            raise ValueError("Customer not found")

        # 3. Extract Customer Features
        features = extract_customer_features(
            db=db,
            national_id=national_id
        )

        if not features or not isinstance(features, dict):
            raise ValueError(
                "Customer features are missing or invalid"
            )

        # 4. Convert Features to DataFrame
        customer_df = pd.DataFrame([features])

        # 5. Check Model Feature Compatibility
        if hasattr(model, "feature_names_in_"):

            expected_features = list(model.feature_names_in_)

            missing_features = [
                feature
                for feature in expected_features
                if feature not in customer_df.columns
            ]

            if missing_features:
                raise ValueError(
                    f"Missing model features: {missing_features}"
                )

            # Ensure feature names and column order
            # match the training configuration.
            customer_df = customer_df[expected_features]

        # 6. Check Model Prediction Support
        if not hasattr(model, "predict_proba"):
            raise ValueError(
                "Model does not support probability prediction"
            )

        # 7. Get Prediction
        prediction = model.predict(customer_df)[0]

        # 8. Identify Default Class
        classes = list(model.classes_)

        if DEFAULT_CLASS not in classes:
            raise ValueError(
                f"Default class {DEFAULT_CLASS} "
                f"not found in model classes: {classes}"
            )

        default_index = classes.index(DEFAULT_CLASS)

        # 9. Calculate Default Probability
        probabilities = model.predict_proba(customer_df)[0]

        probability = float(probabilities[default_index])

        if not isfinite(probability) or not 0 <= probability <= 1:
            raise ValueError(
                "Model returned an invalid default probability"
            )

        # 10. Calculate Risk Score
        risk_score = probability * 100

        # 11. Save Prediction History
        history = Predicthistory(
            customer_id=customer.customer_id,
            prediction=int(prediction),
            default_probability=probability,
            risk_score=risk_score,
            model_version=MODEL_VERSION,
            input_features=features
        )

        db.add(history)
        db.commit()
        db.refresh(history)

        # 12. Return Prediction Result
        return {
            "prediction_id": str(history.prediction_id),
            "prediction": int(prediction),
            "default_probability": round(probability, 4),
            "risk_score": round(risk_score, 2),
            "model_version": MODEL_VERSION,
            "created_at": history.created_at
        }

    except Exception:
        db.rollback()
        raise
