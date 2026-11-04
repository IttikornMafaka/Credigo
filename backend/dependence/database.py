# สร้าง Session ให้แต่ละ API Request และปิด Session เมื่อใช้งานเสร็จ

from app.database.connection import SessionLocal
def get_db() :
    db = SessionLocal()
    try : 
        yield db 
    finally : 
        db.close()