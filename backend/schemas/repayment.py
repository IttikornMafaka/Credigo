from pydantic import BaseModel
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