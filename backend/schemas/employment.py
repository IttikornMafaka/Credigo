from pydantic import BaseModel ,Field 
from uuid import UUID
from datetime import date
from decimal import Decimal

class EmploymentResponse(BaseModel) : 
    employment_id : UUID 
    customer_id : UUID
    company_name : str 
    job_title : str 
    employment_type : str 
    monthly_income : Decimal
    employment_start_date : date 
    
    model_config = {"from_attributes":True}
    
# Add Employment 
class EmploymentCreate(BaseModel):
    
    company_name: str = Field(min_length=1, max_length=150)
    job_title: str = Field(min_length=1, max_length=100)
    employment_type: str = Field(min_length=1, max_length=50)
    monthly_income: Decimal = Field(ge=0)
    employment_start_date: date