from sqlalchemy.orm import Session
from app.model.session import Employment , Customer 
from backend.schemas.employment import EmploymentCreate
from datetime import datetime

def get_employment_by_customerID(db:Session ,customer_id) :
    employment = (db.query(Employment).filter(Employment.customer_id==customer_id).all())
    return employment

def create_employment(db:Session,customer_id,employment_data:EmploymentCreate) : 
    # ตรวจสอบว่ามีลูกค้าคนนี้จริงหรือไม่
    customer = (db.query(Customer).filter(Customer.customer_id == customer_id).first())

    if customer is None:
        return None

    # แปลง date เป็น datetime เพราะ Model ใช้ DateTime
    employment_date = datetime.combine(employment_data.employment_start_date,datetime.min.time())

    new_employment = Employment(
        customer_id=customer_id,
        company_name=employment_data.company_name,
        job_title=employment_data.job_title,
        employment_type=employment_data.employment_type,
        monthly_income=employment_data.monthly_income,
        employment_start_date=employment_date
    )

    try:
        db.add(new_employment)
        db.commit()
        db.refresh(new_employment)
        return new_employment

    except Exception:
        db.rollback()
        raise