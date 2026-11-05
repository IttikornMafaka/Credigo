from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from backend.dependence.database import get_db
from backend.services import validation_service
from backend.schemas.validation import ValidationReport


router = APIRouter(prefix="/api/validation",tags=["Data Validation"])


@router.get("/customer/{customer_id}",response_model=ValidationReport)
def validate_customer(customer_id: UUID,db: Session = Depends(get_db)):
    result = validation_service.validation_data(db,customer_id)

    if result is None:
        raise HTTPException(status_code=404,detail="Customer not found")
    return result