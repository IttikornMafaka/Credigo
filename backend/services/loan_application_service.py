from uuid import UUID

from sqlalchemy.orm import Session

from app.model.session import Customer, LoanApplication
from backend.schemas.loan_application import LoanApplicationCreate


def create_loan_application(db: Session,application_data: LoanApplicationCreate):
    customer = (db.query(Customer).filter(Customer.customer_id == application_data.customer_id).first())

    if not customer:
        raise ValueError("Customer not found")

    new_application = LoanApplication(customer_id=application_data.customer_id,requested_amount=application_data.requested_amount,requested_term_months=application_data.requested_term_months)

    try:
        db.add(new_application)
        db.commit()
        db.refresh(new_application)

        return new_application

    except Exception:
        db.rollback()
        raise


def get_loan_application(db: Session,application_id: UUID):
    return (db.query(LoanApplication).filter(LoanApplication.application_id == application_id).first())


def get_customer_loan_applications(db: Session,customer_id: UUID):
    customer = (db.query(Customer).filter(Customer.customer_id == customer_id).first())

    if not customer:
        raise ValueError("Customer not found")

    return (db.query(LoanApplication).filter(LoanApplication.customer_id == customer_id).order_by(LoanApplication.submitted_at.desc()).all())