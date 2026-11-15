
from sqlalchemy.orm import Session, selectinload

from app.model.session import (
    Customer,
    Loan
)


def get_customer_nationalID(db: Session, national_id: str):
    customer = (
        db.query(Customer)
        .filter(Customer.national_id == national_id)
        .first()
    )
    return customer


def get_customer_by_id(db: Session, customer_id):
    customer = (
        db.query(Customer)
        .filter(Customer.customer_id == customer_id)
        .first()
    )
    return customer


def create_customer(db: Session, customer_data):
    customer = Customer(**customer_data.model_dump())

    db.add(customer)
    db.commit()
    db.refresh(customer)

    return customer


# Get complete customer profile

def get_customer_profile(db: Session, customer_id):

    customer = (
        db.query(Customer)
        .options(
            selectinload(Customer.employment_records),
            selectinload(Customer.accounts),
            selectinload(Customer.credit_histories),
            selectinload(Customer.loans).selectinload(Loan.repayments),
            selectinload(Customer.loan_applications),
            selectinload(Customer.Predict_history)
        )
        .filter(Customer.customer_id == customer_id)
        .first()
    )

    if customer is None:
        return None

    # Collect all repayments from every loan
    repayment_records = [
        repayment
        for loan in customer.loans
        for repayment in loan.repayments
    ]

    # Return customer data with separate repayment records
    profile_data = {
        "customer_id": customer.customer_id,
        "first_name": customer.first_name,
        "last_name": customer.last_name,
        "date_of_birth": customer.date_of_birth,
        "gender": customer.gender,
        "email": customer.email,
        "phone_number": customer.phone_number,
        "national_id": customer.national_id,
        "address": customer.address,
        "marital_status": customer.marital_status,
        "education": customer.education,
        "accounts": customer.accounts,
        "employment_records": customer.employment_records,
        "credit_histories": customer.credit_histories,
        "loans": customer.loans,
        "repayment_records": repayment_records,
        "loan_applications": customer.loan_applications,
        "Predict_history": customer.Predict_history,
        "update_at": customer.update_at
    }

    return profile_data
