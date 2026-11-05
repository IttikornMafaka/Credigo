from sqlalchemy.orm import Session
from app.model.session import Credit

def get_credit_history_by_customerID(db:Session ,customer_id) :
    credit_history = (db.query(Credit).filter(Credit.customer_id==customer_id).all())
    return credit_history