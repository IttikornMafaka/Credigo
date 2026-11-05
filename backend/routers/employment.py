from fastapi import APIRouter,  Depends
from uuid import UUID
from sqlalchemy.orm import Session
from backend.dependence.database import get_db
from backend.services import employment_service
from backend.schemas.employment import EmploymentResponse

router = APIRouter(prefix='/api/employment',tags=['employment']) # prefix กำหนด URL ส่วนต้น (Base Path) ให้กับทุก Endpoint

# Search bank_account by a customer_id
@router.get("/search",response_model=list[EmploymentResponse]) # เราต้องการบัญชีหลายรายการเลยเติม list 

def search_employment(customer_id:UUID, db:Session = Depends(get_db)) :
    employment = employment_service.get_employment_by_customerID(db,customer_id)
    return employment 