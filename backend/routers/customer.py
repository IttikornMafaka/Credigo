from fastapi import APIRouter, HTTPException , Depends
from uuid import UUID
from sqlalchemy.orm import Session
from backend.dependence.database import get_db
from backend.services import customers_service
from backend.schemas.customers import CustomerResponse

router = APIRouter(prefix='/api/customers',tags=['customers']) # prefix กำหนด URL ส่วนต้น (Base Path) ให้กับทุก Endpoint

# Search customer using National ID
@router.get("/search",response_model=CustomerResponse)
def search_customer(national_id:str, db:Session = Depends(get_db)) :
    customer = customers_service.get_customer_nationalID(db,national_id)
    if customer is None :
        raise HTTPException(status_code=404,detail="Customer Not found")
    return customer
# Get customer using Customer UUID
@router.get("/{customer_id}",response_model=CustomerResponse)
def get_customer(customer_id:UUID,db:Session = Depends(get_db)) : 
    customer = customers_service.get_customer_by_id(db,customer_id)
    if customer is None :
        raise HTTPException(status_code=404,detail="Customer Not found ")
    return customer
    