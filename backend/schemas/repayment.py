from pydantic import BaseModel , Field
from uuid import UUID
from datetime import date
from decimal import Decimal 

class Repaymentresponse(BaseModel) : 
    repayment_id : int 
    customer_id : UUID 
    loan_id : int 
    payment_amount : Decimal 
    due_date : date
    payment_date : date  | None = None 
    payment_status : str 
    
    model_config = {"from_attributes":True}
    
    
class RepaymentCreate(BaseModel):
    
    loan_id: int = Field(gt=0)

    payment_amount: Decimal = Field(gt=0)

    due_date: date

    payment_date: date | None = None

    payment_status: str = Field(min_length=1,max_length=30)
