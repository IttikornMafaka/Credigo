from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from backend.dependence.database import get_db
from backend.schemas.prediction import CustomerPredictionRequest
from backend.services.prediction_service import predict_credit_risk



router = APIRouter(
    prefix="/api/predictions",
    tags=["Credit Risk Prediction"]
)


@router.post("/customer")
def predict_customer_risk(request:CustomerPredictionRequest,db:Session = Depends(get_db)):
    try : 
        result = predict_credit_risk(db=db,national_id=request.national_id)
        return {
        "status": "success",
        "message": "Credit risk prediction completed",
        "data": result}
    
    except ValueError as exc:
        if str(exc) == "Customer not found":
            raise HTTPException(status_code=404,detail="Customer not found")

        raise HTTPException(status_code=400,detail=str(exc))
    
    
    