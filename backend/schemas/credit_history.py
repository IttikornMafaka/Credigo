from pydantic import BaseModel , Field
from uuid import UUID
from decimal import Decimal
from datetime import date

class Credithistoryresponse(BaseModel) : 
    credit_id : int 
    customer_id : UUID 
    credit_score : int
    total_debt : Decimal
    credit_utilization : Decimal
    recorded_at : date
    
    model_config = {"from_attributes": True}
    
    

class CreditHistoryCreate(BaseModel):

    credit_score: int = Field(ge=300,le=850)

    total_debt: Decimal = Field(ge=0)

    credit_utilization: Decimal = Field(ge=0,le=100)

    recorded_at: date

