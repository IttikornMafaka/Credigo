from pydantic import BaseModel
from uuid import UUID
from datetime import date

class CustomerResponse(BaseModel) : 
    customer_id: UUID
    first_name: str
    last_name: str
    date_of_birth: date
    gender: str | None = None
    email: str | None = None
    phone_number: str | None = None # ตัวแปรนี้สามารถมีค่าเป็นชนิดข้อมูลที่กำหนด หรือไม่มีค่าก็ได้ | None

    model_config = {"from_attributes": True} # ห้ Pydantic อ่านข้อมูลจาก SQLAlchemy Model ได้โดยตรง