from pydantic import BaseModel
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
    