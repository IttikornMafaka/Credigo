from fastapi import APIRouter, Depends
from uuid import UUID
from sqlalchemy.orm import Session
from backend.dependence.database import get_db
from backend.services import credithistory_service
from backend.schemas.credit_history import  Credithistoryresponse

router = APIRouter(prefix="/api/credit_history",tags=['Credit_history'])

@router.get("/search",response_model=list[Credithistoryresponse])
def get_Credit_history_customer_id(customer_id:UUID,db:Session=Depends(get_db)) :
    credit_history = credithistory_service.get_credit_history_by_customerID(db,customer_id)
    return credit_history