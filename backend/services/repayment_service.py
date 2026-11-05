from sqlalchemy.orm import Session
from app.model.session import Repayment

def get_repayment_by_customer_id(db:Session,customer_id) : 
    repayment = (db.query(Repayment).filter(Repayment.customer_id==customer_id).all())
    return repayment