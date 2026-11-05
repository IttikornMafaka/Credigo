from sqlalchemy.orm import Session
from app.model.session import Account 

def get_account_by_customerID(db:Session ,customer_id) :
    accounts = (db.query(Account).filter(Account.customer_id==customer_id).all())
    return accounts