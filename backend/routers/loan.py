from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from sqlalchemy.orm import Session

from backend.dependence.database import get_db
from backend.services import loan_service
from backend.schemas.loan import LoanCreate, Loanresponse

router = APIRouter(prefix="/api/loan",tags=['loan'])

@router.get("/search",response_model=list[Loanresponse])
def get_customer_loans(customer_id:UUID,db:Session=Depends(get_db)) :
    loans = loan_service.get_loan_customerid(db,customer_id)
    return loans 

@router.post("/{customer_id}",response_model=Loanresponse,status_code=status.HTTP_201_CREATED)
def create_loan(customer_id: UUID,loan_data: LoanCreate,db: Session = Depends(get_db)):
    try:

        new_loan = loan_service.create_loan(
            db,
            customer_id,
            loan_data
        )

        if new_loan is None:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        return new_loan

    except HTTPException:
        raise

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to create loan: {str(exc)}"
        )