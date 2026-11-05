from sqlalchemy.orm import Session
from app.model.session import Loan

def get_loan_customerid(db:Session,customer_id) :
    loan = (db.query(Loan).filter(Loan.customer_id==customer_id).all())
    return loan 
