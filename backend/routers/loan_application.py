from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.dependence.database import get_db
from backend.services import loan_application_service
from backend.schemas.loan_application import LoanApplicationCreate,LoanApplicationResponse

router = APIRouter(prefix="/api/loan-applications",tags=["loan applications"])


# Create new loan application
@router.post("/", response_model=LoanApplicationResponse)
def create_application(application_data: LoanApplicationCreate,db: Session = Depends(get_db)):
    try:
        application = loan_application_service.create_loan_application(db,application_data)
        return application

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# Get application by application_id
@router.get("/{application_id}", response_model=LoanApplicationResponse)
def get_application(application_id: UUID,db: Session = Depends(get_db)):
    
    application = loan_application_service.get_loan_application(db,application_id)

    if not application:
        raise HTTPException(status_code=404,detail="Loan application not found")

    return application


# Get all applications by customer_id
@router.get("/customer/{customer_id}",response_model=list[LoanApplicationResponse])
def get_customer_applications(customer_id: UUID,db: Session = Depends(get_db)):
    try:
        applications = loan_application_service.get_customer_loan_applications(db,customer_id)
        return applications

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))