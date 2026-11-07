from pydantic import BaseModel


class CreditPredictionRequest(BaseModel):
    # Customer Information
    customer_age: int
    gender: str
    marital_status: str
    education: str

    # Employment Information
    employment_type: str
    monthly_income: float
    employment_tenure_months: int

    # Financial Information
    total_account_balance: float
    total_debt: float
    credit_score: float
    credit_utilization: float
    debt_to_income_ratio: float

    # Loan Information
    loan_amount: float
    loan_term_months: int
    loan_purpose: str
    loan_type: str

    # Credit History
    previous_loan_count: int
    late_payment_count: int
    max_days_past_due: int
    previous_default_count: int
    repayment_ratio: float

    class Config:
        extra = "forbid"