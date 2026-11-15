from sqlalchemy.orm import Session

from app.model.session import Repayment, Customer, Loan
from backend.schemas.repayment import RepaymentCreate

def get_repayment_by_customer_id(db:Session,customer_id) : 
    repayment = (db.query(Repayment).filter(Repayment.customer_id==customer_id).all())
    return repayment

def create_repayment(db: Session,customer_id,repayment_data: RepaymentCreate):

    customer = (
        db.query(Customer)
        .filter(Customer.customer_id == customer_id)
        .first()
    )

    if customer is None:
        return None

    # ตรวจสอบว่า Loan มีอยู่จริงและเป็นของลูกค้าคนนี้
    loan = (
        db.query(Loan)
        .filter(
            Loan.loan_id == repayment_data.loan_id,
            Loan.customer_id == customer_id
        )
        .first()
    )

    if loan is None:
        raise ValueError(
            "Loan not found for this customer"
        )

    new_repayment = Repayment(
        customer_id=customer_id,
        loan_id=repayment_data.loan_id,
        payment_amount=repayment_data.payment_amount,
        due_date=repayment_data.due_date,
        payment_date=repayment_data.payment_date,
        payment_status=repayment_data.payment_status
    )

    try:

        db.add(new_repayment)
        db.commit()
        db.refresh(new_repayment)

        return new_repayment

    except Exception:

        db.rollback()
        raise