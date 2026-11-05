from fastapi import APIRouter,  Depends
from uuid import UUID
from sqlalchemy.orm import Session
from backend.dependence.database import get_db
from backend.services import account_service
from backend.schemas.account import AccountResponse

router = APIRouter(prefix='/api/account',tags=['account']) # prefix กำหนด URL ส่วนต้น (Base Path) ให้กับทุก Endpoint

# Search bank_account by a customer_id
@router.get("/search",response_model=list[AccountResponse]) # เราต้องการบัญชีหลายรายการเลยเติม list 

def search_bankaccount(customer_id:UUID, db:Session = Depends(get_db)) :
    accounts = account_service.get_account_by_customerID(db,customer_id)
    return accounts