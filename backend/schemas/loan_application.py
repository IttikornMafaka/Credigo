from datetime import datetime
from uuid import UUID
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict

# Request Schema

class LoanApplicationCreate(BaseModel):
    
    customer_id: UUID

    requested_amount: Decimal = Field(gt=0,description="Requested loan amount")

    requested_term_months: int = Field(gt=0,description="Requested loan term in months")


# Response Schema 

class LoanApplicationResponse(BaseModel):
    
    application_id: UUID
    customer_id: UUID

    requested_amount: Decimal
    requested_term_months: int

    application_status: str
    submitted_at: datetime

    model_config = ConfigDict(from_attributes=True)
 
    
# Schema for Application Status Update

class LoanApplicationStatusUpdate(BaseModel):

    application_status: str = Field(min_length=1,max_length=30)
