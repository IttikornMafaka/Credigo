from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from sqlalchemy.orm import Session

from backend.dependence.database import get_db
from backend.services import repayment_service
from backend.schemas.repayment import Repaymentresponse , RepaymentCreate

router = APIRouter(prefix="/api/repayment",tags=["repayment"])

@router.get("/search",response_model=list[Repaymentresponse])
def get_customer_repayment(customer_id:UUID , db:Session = Depends(get_db)) :
    repayment = repayment_service.get_repayment_by_customer_id(db,customer_id)
    return repayment

@router.post("/{customer_id}",response_model=Repaymentresponse,status_code=status.HTTP_201_CREATED)
def create_repayment(customer_id: UUID,repayment_data: RepaymentCreate,db: Session = Depends(get_db)):
    try:

        new_repayment = repayment_service.create_repayment(
            db,
            customer_id,
            repayment_data
        )

        if new_repayment is None:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        return new_repayment

    except ValueError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc)
        )

    except HTTPException:
        raise

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to create repayment: {str(exc)}"
        )