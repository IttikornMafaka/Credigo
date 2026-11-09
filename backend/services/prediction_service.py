
import joblib
import pandas as pd
from sqlalchemy import text
from pathlib import Path
from sqlalchemy.orm import Session

from backend.services.feature_service import extract_customer_features
from app.model.session import Customer, Predicthistory


# =====================================================
# Load Random Forest Model
# =====================================================

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = BASE_DIR / "ml_training" / "random_forest_model.pkl"

model = joblib.load(MODEL_PATH)

MODEL_VERSION = "random_forest_v1"


# =====================================================
# Credit Risk Prediction + History
# =====================================================

def predict_credit_risk(db: Session, national_id: str):

    try:
        
        
        # ตรวจสอบ Database ที่ FastAPI เชื่อมต่ออยู่
        result = db.execute(text("""
            SELECT
                current_database(),
                current_schema(),
                current_user,
                inet_server_addr(),
                inet_server_port(),
                to_regclass('public.prediction_history')
        """)).fetchone()

        print("FASTAPI DATABASE:", result,flush=True)
        

        
        # 1. Extract customer features
        features = extract_customer_features(
            db=db,
            national_id=national_id
        )

        # 2. Find customer
        customer = db.query(Customer).filter(
            Customer.national_id == national_id
        ).first()

        if customer is None:
            raise ValueError("Customer not found")

        # 3. Convert features to DataFrame
        customer_df = pd.DataFrame([features])

        # 4. Random Forest Prediction
        prediction = model.predict(customer_df)[0]

        # 5. Calculate default probability
        classes = list(model.classes_)
        default_index = classes.index(1)

        probability = model.predict_proba(customer_df)[0][default_index]

        # 6. Calculate risk score
        risk_score = probability * 100

        # 7. Save prediction history
        history = Predicthistory(
            customer_id=customer.customer_id,
            prediction=int(prediction),
            default_probability=float(probability),
            risk_score=float(risk_score),
            model_version=MODEL_VERSION,
            input_features=features
        )

        db.add(history)
        db.commit()
        db.refresh(history)

        # 8. Return result
        return {
            "prediction_id": str(history.prediction_id),
            "prediction": int(prediction),
            "default_probability": round(float(probability), 4),
            "risk_score": round(float(risk_score), 2),
            "model_version": MODEL_VERSION,
            "created_at": history.created_at
        }

    except Exception:
        db.rollback()
        raise
    
    