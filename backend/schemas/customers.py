from pydantic import BaseModel , Field
from uuid import UUID
from datetime import date , datetime
from decimal import Decimal 

class CustomerResponse(BaseModel) : 
    customer_id: UUID
    first_name: str
    last_name: str
    date_of_birth: date
    gender: str | None = None
    email: str | None = None
    phone_number: str | None = None # ตัวแปรนี้สามารถมีค่าเป็นชนิดข้อมูลที่กำหนด หรือไม่มีค่าก็ได้ | None

    model_config = {"from_attributes": True} # ให้ Pydantic อ่านข้อมูลจาก SQLAlchemy Model ได้โดยตรง
    

class CustomerCreate(BaseModel):
    
    national_id: str = Field(min_length=13,max_length=13,pattern=r"^\d{13}$")
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    date_of_birth: date

    gender: str | None = None
    email: str | None = None
    phone_number: str | None = None
    address: str | None = None
    marital_status: str | None = None
    education: str | None = None
    
# ==============================
# Customer Profile Schemas
# ==============================

class AccountResponse(BaseModel):
    account_id: UUID
    account_number: str
    bank_name: str
    account_type: str | None = None
    balance: Decimal | None = None
    account_status: str | None = None
    opened_at: datetime | None = None

    model_config = {"from_attributes": True}


class EmploymentResponse(BaseModel):
    employment_id: UUID
    company_name: str | None = None
    job_title: str | None = None
    employment_type: str | None = None
    monthly_income: Decimal | None = None
    employment_start_date: datetime | None = None

    model_config = {"from_attributes": True}


class CreditHistoryResponse(BaseModel):
    credit_id: int
    customer_id: UUID
    credit_score: int | None = None
    total_debt: Decimal | None = None
    credit_utilization: Decimal | None = None
    recorded_at: datetime | None = None

    model_config = {"from_attributes": True}


class RepaymentResponse(BaseModel):
    repayment_id: int
    loan_id: int
    payment_amount: Decimal
    due_date: date
    payment_date: date | None = None
    payment_status: str

    model_config = {"from_attributes": True}


class LoanResponse(BaseModel):
    loan_id: int
    loan_amount: Decimal
    interest_rate: Decimal
    loan_term: int
    loan_status: str
    application_date: datetime | None = None

    repayments: list[RepaymentResponse] = []

    model_config = {"from_attributes": True}


class LoanApplicationResponse(BaseModel):
    application_id: UUID
    requested_amount: Decimal
    requested_term_months: int
    application_status: str
    submitted_at: datetime

    model_config = {"from_attributes": True}


class PredictionHistoryResponse(BaseModel):
    prediction_id: UUID
    prediction: int
    default_probability: float
    risk_score: float
    model_version: str
    input_features: dict
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


# Complete Customer Profile


# Complete Customer Profile

class CustomerProfileResponse(CustomerResponse):

    national_id: str
    address: str | None = None
    marital_status: str | None = None
    education: str | None = None

    accounts: list[AccountResponse] = []
    employment_records: list[EmploymentResponse] = []
    credit_histories: list[CreditHistoryResponse] = []

    loans: list[LoanResponse] = []

    # Add separate repayment records
    repayment_records: list[RepaymentResponse] = []

    loan_applications: list[LoanApplicationResponse] = []
    Predict_history: list[PredictionHistoryResponse] = []

    update_at: datetime | None = None

    
    
# Create Customer Records

# 1. Employment
class EmploymentCreate(BaseModel):
    company_name: str | None = None
    job_title: str | None = None
    employment_type: str | None = None
    monthly_income: Decimal | None = Field(default=None, ge=0)
    employment_start_date: datetime | None = None
    
# 2. Bank Account
class AccountCreate(BaseModel):
    account_number: str = Field(min_length=1, max_length=50)
    bank_name: str = Field(min_length=1, max_length=100)
    account_type: str | None = None
    balance: Decimal = Field(default=0, ge=0)
    account_status: str | None = None
    opened_at: datetime | None = None
    
# 3. Credit History
class CreditHistoryCreate(BaseModel):
    credit_score: int | None = Field(default=None, ge=0, le=1000)
    total_debt: Decimal = Field(default=0, ge=0)
    credit_utilization: Decimal | None = Field(
        default=None, ge=0, le=100
    )
    recorded_at: datetime | None = None


# 4. Loan
class LoanCreate(BaseModel):
    loan_amount: Decimal = Field(gt=0)
    interest_rate: Decimal = Field(ge=0)
    loan_term: int = Field(gt=0)
    loan_status: str
    application_date: datetime | None = None


# 5. Repayment
class RepaymentCreate(BaseModel):
    loan_id: int
    payment_amount: Decimal = Field(gt=0)
    due_date: date
    payment_date: date | None = None
    payment_status: str


# 6. Loan Application
class LoanApplicationCreate(BaseModel):
    requested_amount: Decimal = Field(gt=0)
    requested_term_months: int = Field(gt=0)
    application_status: str = "Submitted"