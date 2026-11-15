
from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from sqlalchemy.orm import Session

from backend.dependence.database import get_db
from backend.services import credithistory_service
from backend.schemas.credit_history import (
    Credithistoryresponse,
    CreditHistoryCreate
)

router = APIRouter(
    prefix="/api/credit-history",
    tags=["Credit History"]
)

# Search credit history using customer_id
@router.get("/search", response_model=list[Credithistoryresponse])
def get_credit_history_customer_id(
    customer_id: UUID,
    db: Session = Depends(get_db)
):
    credit_history = credithistory_service.get_credit_history_by_customerID(
        db, customer_id
    )
    return credit_history


# Create credit history
@router.post("/{customer_id}",response_model=Credithistoryresponse,status_code=status.HTTP_201_CREATED)
def create_credit_history(customer_id: UUID,credit_data: CreditHistoryCreate,db: Session = Depends(get_db)):
    try:
        new_credit = credithistory_service.create_credit_history(
            db, customer_id, credit_data
        )

        if new_credit is None:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        return new_credit

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create credit history: {str(exc)}"
        )
