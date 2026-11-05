from pydantic import BaseModel
from uuid import UUID
from datetime import date
from decimal import Decimal 

class AccountResponse(BaseModel) :
    account_id : UUID  
    customer_id : UUID 
    account_number : str
    bank_name : str 
    account_type : str 
    balance : Decimal | None = None 
    account_status : str | None = None   
    opened_at : date | None = None 
    
    model_config = {"from_attributes":True}
    
