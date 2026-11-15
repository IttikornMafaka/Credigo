from pydantic import BaseModel , Field
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
    
class AccountCreate(BaseModel) : 
    
    account_number: str = Field(min_length=1,max_length=50)
    bank_name: str = Field(min_length=1,max_length=100)
    account_type: str = Field(min_length=1,max_length=50)
    balance: Decimal = Field(ge=0)
    account_status: str = Field(min_length=1,max_length=30)
    opened_at : date
