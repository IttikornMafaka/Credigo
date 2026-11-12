from datetime import date
from uuid import UUID
from sqlalchemy.orm import Session
from app.model.session import Credit , Customer , Account , Loan ,Repayment ,Employment 
from backend.schemas.validation import ValidationIssues , ValidationReport
from sqlalchemy import func

def validation_data (db:Session,customer_id:UUID) : 
    # Search Customer Data 
    customer = (db.query(Customer).filter(Customer.customer_id==customer_id).first()) 
    if not customer : 
        return None 
    issues = []
    total_checks = 0
    passed = 0
    failed = 0 
    
    def check(condition,rule_id,table,field,message) :  # เช็คตามฟังก์ชั่น
        nonlocal total_checks , passed , failed  
        total_checks += 1 
        if condition : 
            passed += 1 
        else :
            failed += 1
            issues.append(ValidationIssues(rule_id=rule_id,table=table,field=field,severity="ERROR",message=message))
            
    def is_missing(value) :
        if value is None :
            return True 
        if isinstance(value,str) and value.strip() == "" :
            return True 
        return False 
    
    # Check Customer
    check(customer.date_of_birth is not None and customer.date_of_birth <= date.today(),"CUS001","customers_detail","date_of_birth","Date of birth is missing or cannot be in the future") 
    
    if customer :
        check(not is_missing(customer.national_id),"CUS002","customers_detail","national_id","National ID is missing")
        check(not is_missing(customer.first_name),"CUS003","customers_detail","first_name","First name is missing")
        check(not is_missing(customer.last_name),"CUS004","customers_detail","last_name","Last name is missing")
    
    # Check Account 
    accounts = (db.query(Account).filter(Account.customer_id==customer_id).all())
    for account in accounts : 
        check(account.balance is not None,"ACC002","accounts","balance","Account balance is missing")
        
        if account.balance is not None:
            check(account.balance >= 0,"ACC001","accounts","balance","Account balance is negative")
            
        check(not is_missing(account.account_number),"CUS002","accounts","account_number","Account number is missing")
        check(not is_missing(account.bank_name),"CUS002","accounts","bank_name","Bank name is missing")
        # Check Duplicate account
        duplicate_account = (db.query(Account.customer_id,Account.account_number).filter(Account.customer_id==customer_id).group_by(Account.customer_id,Account.account_number).having(func.count(Account.account_id)>1).all())
        for duplicate in duplicate_account :
            check(False,"ACC005","accounts","account_number",f"Duplicate account number found: {duplicate.account_number}")
            
    # Check Loan 
    loans = (db.query(Loan).filter(Loan.customer_id==customer_id).all())
    for loan in loans :
        check(loan.loan_amount > 0,"LOAN001","loans","loan_amount","Loan amount must be greater than zero")
        check(loan.interest_rate >= 0,"LOAN002","loans","interest_rate","Interest rate cannot be negative") # ตรวจดอกเบี้ย
        check(loan.loan_term is not None and loan.loan_term > 0,"LOAN003","loans","loan_term","Loan term must be greater than zero")
        check(not is_missing(loan.loan_status),"LOAN003","loans","loan_term","Loan status missing")
        
        # Check Relationship loan and customer (Referential Integrity Check การตรวจสอบความถูกต้องของความสัมพันธ์ระหว่างตาราง)
        customer = (db.query(Customer).filter(Customer.customer_id==Loan.customer_id).first())
        if customer is None : 
             check(False,"CON002","loans","customer_id","Referenced customer does not exist")
            
        # Check Bussiness Rule : Application Date
        check(loan.application_date is not None and loan.application_date<= date.today(),"LOAN005","loans","application_date","Loan application date cannot be in the future")
        

    # Check Repayments
    repayments = (db.query(Repayment).filter(Repayment.customer_id == customer_id).all())
    for repayment in repayments : 
        check(repayment.payment_amount >= 0,"REP001","repayment_records","payment_amount","Payment amount cannot be negative")
        check(not is_missing(repayment.payment_status),"REP002","repayment_records","payment_status","Payment status missing")
        check(repayment.due_date is not None,"REP003","repayment_records","due_date","Due date is missing")
        
        # Check Relationship repayment and loan (Referential Integrity Check การตรวจสอบความถูกต้องของความสัมพันธ์ระหว่างตาราง)
        loan = (db.query(Loan).filter(Loan.loan_id==repayment.loan_id).first())
        if loan is None or loan.customer_id != customer_id: 
            check(False,"CON001","repayment_records","loan_id","Repayment references a missing loan or a loan belonging to another customer")
            
    # Check Employment
    employments = (db.query(Employment).filter(Employment.customer_id==customer_id).all())
    for employment in employments : 
        check(employment.monthly_income is not None,"EMP002","employment_records","monthly_income","Monthly income is missing")
        
        if employment.monthly_income is not None:
            check(employment.monthly_income >= 0,"EMP001","employment_records","monthly_income","Monthly income cannot be negative")
        
    # Check Credit History
    credits = (db.query(Credit).filter(Credit.customer_id==customer_id).all())
    for credit in credits : 
        check(credit.total_debt >= 0,"CRD001","credit_history","total_debt","Total debt cannot be negative")
        check(credit.credit_score is not None,"CRD002","credit_history","credit_score","Credit score is missing")
        check(credit.recorded_at is not None,"CRD003","credit_history","recorded_at","Credit history recording date is missing")


    # Summarize
    overall_status = ("NEEDS_REVIEW" if failed > 0 else "PASS")

    return ValidationReport(customer_id=customer_id,total_checks=total_checks,passed=passed,failed=failed,overall_status=overall_status,issues=issues)
