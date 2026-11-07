from fastapi import APIRouter

from backend.schemas.prediction import CreditPredictionRequest
from backend.services.prediction_service import predict_credit_risk


router = APIRouter(
    prefix="/api/predictions",
    tags=["Credit Risk Prediction"]
)


@router.post("/customer")
def predict_customer_risk(customer_data: CreditPredictionRequest):
    result = predict_credit_risk(customer_data)

    return {
        "status": "success",
        "message": "Credit risk prediction completed",
        "data": result
    }