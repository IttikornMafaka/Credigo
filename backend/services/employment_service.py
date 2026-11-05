from sqlalchemy.orm import Session
from app.model.session import Employment

def get_employment_by_customerID(db:Session ,customer_id) :
    employment = (db.query(Employment).filter(Employment.customer_id==customer_id).all())
    return employment