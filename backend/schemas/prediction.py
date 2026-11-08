from pydantic import BaseModel , Field



class CustomerPredictionRequest(BaseModel):
    national_id: str = Field(...,min_length=13,max_length=13,description="Customer's 13-digit national ID")

    class Config:
        extra = "forbid"