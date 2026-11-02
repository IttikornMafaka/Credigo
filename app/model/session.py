import uuid

from sqlalchemy import (Column,Integer,String,Date,DateTime,Numeric,BigInteger,ForeignKey,Uuid)

from sqlalchemy.orm import relationship

from app.database.connection import Base


class Customer(Base) : 
   __tablename__ = "customers_detail"
   customer_id = Column(Uuid(as_uuid=True),primary_key=True,default=uuid.uuid4)
   national_id = Column(String(13), unique=True, nullable=False)
   first_name = Column(String(100), nullable=False)
   last_name = Column(String(100), nullable=False)
   date_of_birth = Column(Date, nullable=False)
   gender = Column(String(20))
   phone_number = Column(String(20))
   email = Column(String(255))
   address = Column(String(500))
   marital_status = Column(String(30))
   education = Column(String(100))
   updated_at = Column(DateTime)

   # Relationships
   accounts = relationship("Account", back_populates="customer")
   credit_histories = relationship("Credit", back_populates="customer")
   employment_records = relationship("Employment", back_populates="customer")
   loans = relationship("Loan", back_populates="customer")

    
class Account(Base):
    __tablename__ = "accounts"
    account_id = Column(Uuid(as_uuid=True),primary_key=True,default=uuid.uuid4)
    customer_id = Column(Uuid(as_uuid=True),ForeignKey("customers_detail.customer_id"),nullable=False)
    account_number = Column(String(50), nullable=False)
    bank_name = Column(String(100), nullable=False)
    account_type = Column(String(50))
    balance  = Column(Numeric(15, 2), default=0)
    account_status = Column(String(30))
    opened_at = Column(DateTime)
    
    customer = relationship("Customer", back_populates="accounts")
    
class Credit(Base) : 
    __tablename__ = "credit_history"
    credit_id = Column(Uuid(as_uuid=True),primary_key=True,default=uuid.uuid4)
    customer_id = Column(Uuid(as_uuid=True),ForeignKey("customers_detail.customer_id"),nullable=False)
    credit_score = Column(Integer)
    total_debt = Column(Numeric(15, 2), default=0)
    credit_utilization = Column(Numeric(5, 2))
    recorded_at = Column(DateTime)
    
    customer = relationship("Customer", back_populates="credit_histories")
    
class Employment(Base) : 
    __tablename__ = "employment_records"
    employment_id = Column(Uuid(as_uuid=True),primary_key=True,default=uuid.uuid4)
    customer_id = Column(Uuid(as_uuid=True),ForeignKey("customers_detail.customer_id"),nullable=False)
    company_name = Column(String(150))
    job_title = Column(String(100))
    employment_type = Column(String(50))
    monthly_income = Column(Numeric(15,2))
    employment_start_date = Column(DateTime)
    
    customer = relationship("Customer", back_populates="employment_records")
    
class Loan(Base) :
    __tablename__ = "loans"
    loan_id = Column(BigInteger,primary_key=True,autoincrement=True)
    customer_id = Column(Uuid(as_uuid=True),ForeignKey("customers_detail.customer_id"),nullable=False)
    loan_amount = Column(Numeric(15, 2), nullable=False)
    interest_rate = Column(Numeric(5, 2), nullable=False)
    loan_term = Column(Integer, nullable=False)
    loan_status = Column(String(30), nullable=False)
    application_date = Column(DateTime)
    
    customer = relationship("Customer", back_populates="loans")
    repayments = relationship("Repayment", back_populates="loan")
    
class Repayment(Base) : 
    __tablename__ = "repayment_records" 
    repayment_id = Column(BigInteger,primary_key=True,autoincrement=True)
    customer_id = Column(Uuid(as_uuid=True),ForeignKey("customers_detail.customer_id"),nullable=False)
    loan_id = Column(BigInteger,ForeignKey("loans.loan_id"),nullable=False)
    payment_amount =  Column(Numeric(15, 2), nullable=False)
    due_date = Column(Date, nullable=False)
    payment_date = Column(Date, nullable=True)
    payment_status = Column(String(30), nullable=False)
    
    loan = relationship("Loan", back_populates="repayments")