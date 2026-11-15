from fastapi import APIRouter,  Depends , HTTPException, status
from uuid import UUID
from sqlalchemy.orm import Session
from backend.dependence.database import get_db
from backend.services import employment_service
from backend.schemas.employment import EmploymentResponse , EmploymentCreate

router = APIRouter(prefix='/api/employment',tags=['employment']) # prefix กำหนด URL ส่วนต้น (Base Path) ให้กับทุก Endpoint

# Search bank_account by a customer_id
@router.get("/search",response_model=list[EmploymentResponse]) # เราต้องการบัญชีหลายรายการเลยเติม list 
def search_employment(customer_id:UUID, db:Session = Depends(get_db)) :
    employment = employment_service.get_employment_by_customerID(db,customer_id)
    return employment 

# Create Employment Record
@router.post("/{customer_id}",response_model=EmploymentResponse,status_code=status.HTTP_201_CREATED)
def create_employment(customer_id: UUID,employment_data: EmploymentCreate,db: Session = Depends(get_db)):
    try:
        new_employment = employment_service.create_employment(db,customer_id,employment_data)

        if new_employment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )

        return new_employment

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create employment record"
        )