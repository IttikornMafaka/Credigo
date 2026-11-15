from pydantic import BaseModel , Field
from uuid import UUID
from datetime import date
from decimal import Decimal 

class Loanresponse(BaseModel) : 
    loan_id : int 
    customer_id : UUID 
    loan_amount : Decimal
    interest_rate : Decimal
    loan_term : int 
    loan_status : str 
    application_date : date 
    
    model_config = {"from_attributes":True}
    
    
class LoanCreate(BaseModel):
    
    loan_amount: Decimal = Field(gt=0)

    interest_rate: Decimal = Field(ge=0,le=100)

    loan_term: int = Field(gt=0,le=600)

    loan_status: str = Field(min_length=1,max_length=30)

    application_date: date