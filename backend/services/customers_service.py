from sqlalchemy.orm import Session
from app.model.session import Customer

def get_customer_nationalID(db:Session , national_id:str) :
    customer = (db.query(Customer).filter(Customer.national_id==national_id).first()) #.first คืนข้อมูลลูกค้ารายแรกที่พบ
    return customer

def get_customer_by_id(db:Session,customer_id) :
    customer = (db.query(Customer).filter(Customer.customer_id==customer_id).first()) #.first คืนข้อมูลลูกค้ารายแรกที่พบ
    return customer 