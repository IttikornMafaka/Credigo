from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from decimal import Decimal

class Credithistoryresponse(BaseModel) : 
    credit_id : int 
    customer_id : UUID 
    credit_score : int
    total_debt : Decimal
    credit_utilization : Decimal
    recorded_at : datetime
    
    model_config = {"from_attributes": True}