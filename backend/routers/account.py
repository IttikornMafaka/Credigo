from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from sqlalchemy.orm import Session

from backend.dependence.database import get_db
from backend.services import account_service
from backend.schemas.account import AccountResponse, AccountCreate

router = APIRouter(prefix='/api/account',tags=['account']) # prefix กำหนด URL ส่วนต้น (Base Path) ให้กับทุก Endpoint

# Search bank_account by a customer_id
@router.get("/search",response_model=list[AccountResponse]) # เราต้องการบัญชีหลายรายการเลยเติม list 

def search_bankaccount(customer_id:UUID, db:Session = Depends(get_db)) :
    accounts = account_service.get_account_by_customerID(db,customer_id)
    return accounts

@router.post("/{customer_id}",response_model=AccountResponse,status_code=status.HTTP_201_CREATED)
def create_bankaccount(customer_id: UUID,account_data: AccountCreate,db: Session = Depends(get_db)):

    try:

        new_account = account_service.create_account(
            db,
            customer_id,
            account_data
        )

        if new_account is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )

        return new_account

    except HTTPException:
        raise

    except Exception as exc:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create bank account: {str(exc)}"
        )