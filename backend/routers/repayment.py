from fastapi import APIRouter, Depends
from uuid import UUID
from sqlalchemy.orm import Session
from backend.dependence.database import get_db
from backend.services import repayment_service
from backend.schemas.repayment import Repaymentresponse

router = APIRouter(prefix="/api/repayment",tags=["repayment"])

@router.get("/search",response_model=list[Repaymentresponse])
def get_customer_repayment(customer_id:UUID , db:Session = Depends(get_db)) :
    repayment = repayment_service.get_repayment_by_customer_id(db,customer_id)
    return repayment
