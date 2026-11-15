from datetime import date
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
    submitted_at: date

    model_config = ConfigDict(from_attributes=True)
 
    
# Schema for Application Status Update

class LoanApplicationStatusUpdate(BaseModel):

    application_status: str = Field(min_length=1,max_length=30)


class LoanApplicationCreate(BaseModel):
    
    requested_amount: Decimal = Field(gt=0)

    requested_term_months: int = Field(gt=0,le=600)

    application_status: str = Field(default="Submitted",min_length=1,max_length=30)
