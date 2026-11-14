from datetime import date, datetime

from sqlalchemy.orm import Session
from sqlalchemy import func
from uuid import UUID 
from app.model.session import Customer,Account,Credit,Employment,Loan,Repayment,LoanApplication

def calculate_age(birth_date):
    today = date.today()

    return (
        today.year - birth_date.year
        - ((today.month, today.day) < (birth_date.month, birth_date.day))
    )


def calculate_employment_tenure(start_date):
    today = date.today()

    months = (
        (today.year - start_date.year) * 12
        + today.month - start_date.month
    )

    return max(months, 0)

def normalize_marital_status(value):
    if value is None:
        return None

    value = str(value).strip().lower()

    mapping = {
        "s": "Single",
        "single": "Single",

        "m": "Married",
        "married": "Married",

        "d": "Divorced",
        "divorced": "Divorced",

        "w": "Widowed",
        "widowed": "Widowed"
    }
    return mapping.get(value,value)


def normalize_education(value):
    if value is None:
        return None

    value = str(value).strip().lower()

    mapping = {
        "b": "Bachelor",
        "bachelor": "Bachelor",
        "diploma": "Diploma",
        "doctorate": "Doctorate",
        "h": "High School",
        "high school": "High School",
        "m": "Master",
        "master": "Master"
    }

    return mapping.get(value, value)


def normalize_employment_type(value):
    if value is None:
        return None

    value = str(value).strip().lower()

    mapping = {
        "freelance": "Freelance",
        "full-time": "Full-time",
        "part-time": "Part-time",
        "self-employed": "Self-employed",
        "unemployed": "Unemployed",
        "contract": "Full-time"
    }

    return mapping.get(value, value)

def extract_customer_features(db: Session,national_id: str):
    
    # 1. Find customer
    customer = (
        db.query(Customer)
        .filter(Customer.national_id == national_id)
        .first()
    )

    if not customer:
        raise ValueError("Customer not found")
    
    if customer.marital_status is None:
         raise ValueError("Missing marital status")

    # 2. Get latest employment record
    employment = (
        db.query(Employment)
        .filter(Employment.customer_id == customer.customer_id)
        .order_by(Employment.employment_start_date.desc())
        .first()
    )

    # 3. Get latest credit record
    credit = (
        db.query(Credit)
        .filter(Credit.customer_id == customer.customer_id)
        .order_by(Credit.recorded_at.desc())
        .first()
    )

    # 4. Calculate total account balance
    total_balance = (
        db.query(func.coalesce(func.sum(Account.balance), 0))
        .filter(Account.customer_id == customer.customer_id)
        .scalar()
    )

    # 5. Get latest loan
    latest_loan = (
        db.query(Loan)
        .filter(Loan.customer_id == customer.customer_id)
        .order_by(Loan.application_date.desc())
        .first()
    )

    # 6. Count previous loans
    previous_loan_count = (
        db.query(func.count(Loan.loan_id))
        .filter(Loan.customer_id == customer.customer_id)
        .scalar()
    )

    # 7. Count late and missed payments
    late_payment_count = (
        db.query(func.count(Repayment.repayment_id))
        .filter(
            Repayment.customer_id == customer.customer_id,
            Repayment.payment_status.in_(["Late", "Missed"])
        )
        .scalar()
    )

    # 8. Calculate customer age
    customer_age = calculate_age(customer.date_of_birth)

    # 9. Calculate employment tenure
    if employment and employment.employment_start_date:
        employment_tenure = calculate_employment_tenure(
            employment.employment_start_date
        )
    else:
        employment_tenure = 0

    # 10. Build ML Features
    features = {
        "customer_age": customer_age,
        "marital_status": normalize_marital_status(customer.marital_status),
        "education": normalize_education(customer.education),
        "employment_type": (normalize_employment_type(employment.employment_type)
        if employment else None
        ),

        "monthly_income": (
            float(employment.monthly_income)
            if employment and employment.monthly_income is not None
            else 0.0
        ),

        "employment_tenure_months": employment_tenure,

        "total_account_balance": float(total_balance or 0),

        "total_debt": (
            float(credit.total_debt)
            if credit and credit.total_debt is not None
            else 0.0
        ),

        "credit_score": credit.credit_score if credit else 0,

        "credit_utilization": (
            float(credit.credit_utilization)
            if credit and credit.credit_utilization is not None
            else 0.0
        ),

        "loan_amount": (
            float(latest_loan.loan_amount)
            if latest_loan else 0.0
        ),

        "loan_term_months": (
            latest_loan.loan_term if latest_loan else 0
        ),

        "previous_loan_count": previous_loan_count or 0,

        "late_payment_count": late_payment_count or 0
    }
    
    print("MARITAL:", repr(features["marital_status"]))
    print("EDUCATION:", repr(features["education"]))
    print("EMPLOYMENT:", repr(features["employment_type"]))

    # Validate employment type for Model V1
    allowed_employment_types = {
        "Freelance",
        "Full-time",
        "Part-time",
        "Self-employed",
        "Unemployed"
    }

    employment_type = features["employment_type"]

    if employment_type is None:
        raise ValueError("Missing employment type")

    if employment_type not in allowed_employment_types:
        raise ValueError(
            f"Unsupported employment type: {employment_type}. "
            "Manual review required."
        )

    return features

def extract_application_evidence(
    db: Session,
    national_id: str,
    application_id: UUID
):
    # 1. Find customer
    customer = (
        db.query(Customer)
        .filter(Customer.national_id == national_id)
        .first()
    )

    if not customer:
        raise ValueError("Customer not found")

    # 2. Find loan application belonging to this customer
    application = (
        db.query(LoanApplication)
        .filter(
            LoanApplication.application_id == application_id,
            LoanApplication.customer_id == customer.customer_id
        )
        .first()
    )

    if not application:
        raise ValueError(
            "Loan application not found for this customer"
        )

    # 3. Extract application evidence
    evidence = {
        "application_id": application.application_id,
        "customer_id": customer.customer_id,
        "requested_amount": application.requested_amount,
        "requested_term_months": application.requested_term_months,
        "application_status": application.application_status,
        "submitted_at": application.submitted_at
    }

    return evidence