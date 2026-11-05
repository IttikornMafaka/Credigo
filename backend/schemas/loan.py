from pydantic import BaseModel
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