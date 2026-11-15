from fastapi import APIRouter, HTTPException, Depends
from fastapi import status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from uuid import UUID

from backend.dependence.database import get_db
from backend.services import customers_service
from backend.schemas.customers import CustomerResponse, CustomerCreate , CustomerProfileResponse

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


@router.post("/",response_model=CustomerResponse,status_code=status.HTTP_201_CREATED)
def register_customer(customer_data: CustomerCreate,db: Session = Depends(get_db)):
    # 1. Check National ID again 
    existing_customer = customers_service.get_customer_nationalID(db,customer_data.national_id)

    if existing_customer:
        raise HTTPException(status_code=409,detail="National ID already registered")

    # 2. Save customer data 
    try:
        customer = customers_service.create_customer(db,customer_data)
        return customer

    except IntegrityError as e:
        db.rollback()

        print("\n========== CREDIGO DATABASE ERROR ==========")
        print("ERROR:", repr(e.orig))
        print("============================================\n")

        raise HTTPException(status_code=409,detail="Database integrity error")
    
    
# Get complete Customer Profile
@router.get("/{customer_id}/profile",response_model=CustomerProfileResponse)
def get_customer_profile(customer_id: UUID,db: Session = Depends(get_db)):
    customer = customers_service.get_customer_profile(
        db,
        customer_id
    )

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer Profile Not Found"
        )

    return customer