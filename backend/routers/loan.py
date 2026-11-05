from fastapi import APIRouter, Depends
from uuid import UUID
from sqlalchemy.orm import Session
from backend.dependence.database import get_db
from backend.services import loan_service
from backend.schemas.loan import Loanresponse

router = APIRouter(prefix="/api/loan",tags=['loan'])

@router.get("/search",response_model=list[Loanresponse])
def get_customer_loans(customer_id:UUID,db:Session=Depends(get_db)) :
    loans = loan_service.get_loan_customerid(db,customer_id)
    return loans 