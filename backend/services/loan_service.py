from sqlalchemy.orm import Session

from app.model.session import Loan, Customer
from backend.schemas.loan import LoanCreate

def get_loan_customerid(db:Session,customer_id) :
    loan = (db.query(Loan).filter(Loan.customer_id==customer_id).all())
    return loan 

def create_loan(db: Session,customer_id,loan_data: LoanCreate):

    customer = (db.query(Customer).filter(Customer.customer_id == customer_id).first())

    if customer is None:
        return None

    new_loan = Loan(
        customer_id=customer_id,
        loan_amount=loan_data.loan_amount,
        interest_rate=loan_data.interest_rate,
        loan_term=loan_data.loan_term,
        loan_status=loan_data.loan_status,
        application_date=loan_data.application_date
    )

    try:

        db.add(new_loan)
        db.commit()
        db.refresh(new_loan)

        return new_loan

    except Exception:

        db.rollback()
        raise