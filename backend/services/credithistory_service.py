from sqlalchemy.orm import Session

from app.model.session import Credit, Customer
from backend.schemas.credit_history import CreditHistoryCreate

def get_credit_history_by_customerID(db:Session ,customer_id) :
    credit_history = (db.query(Credit).filter(Credit.customer_id==customer_id).all())
    return credit_history


def create_credit_history(db: Session,customer_id,credit_data: CreditHistoryCreate):

    customer = (db.query(Customer).filter(Customer.customer_id == customer_id).first())

    if customer is None:
        return None

    new_credit = Credit(
        customer_id=customer_id,
        credit_score=credit_data.credit_score,
        total_debt=credit_data.total_debt,
        credit_utilization=credit_data.credit_utilization,
        recorded_at=credit_data.recorded_at
    )

    try:

        db.add(new_credit)
        db.commit()
        db.refresh(new_credit)

        return new_credit

    except Exception:

        db.rollback()
        raise