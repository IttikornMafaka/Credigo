from datetime import date
from uuid import UUID
from sqlalchemy.orm import Session
from app.model.session import Credit , Customer , Account , Loan ,Repayment ,Employment 
from backend.schemas.validation import ValidationIssues , ValidationReport

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
    
    # Check Customer
    check(customer.date_of_birth <= date.today(),"CUS001","customers_detail","date_of_birth","Date of birth cannot be in the future") 
    
    # Check Account 
    accounts = (db.query(Account).filter(Account.customer_id==customer_id).all())
    for account in accounts : 
        check(account.balance>= 0,   "ACC001","accounts","balance","Account balance is negative")
        
    # Check Loan 
    loans = (db.query(Loan).filter(Loan.customer_id==customer_id).all())
    for loan in loans :
        check(loan.loan_amount > 0,"LOAN001","loans","loan_amount","Loan amount must be greater than zero")
        check(loan.interest_rate >= 0,"LOAN002","loans","interest_rate","Interest rate cannot be negative") # ตรวจดอกเบี้ย

    # Check Repayments
    repayments = (db.query(Repayment).filter(Repayment.customer_id == customer_id).all())
    for repayment in repayments : 
        check(repayment.payment_amount >= 0,"REP001","repayment_records","payment_amount","Payment amount cannot be negative")
        
    # Check Employment
    employments = (db.query(Employment).filter(Employment.customer_id==customer_id).all())
    for employment in employments : 
        check(employment.monthly_income >= 0 , "EMP001","employment_records","monthly_income","Monthly income cannot be negative")
        
    # Check Credit History
    credits = (db.query(Credit).filter(Credit.customer_id==customer_id).all())
    for credit in credits : 
        check(credit.total_debt >= 0,"CRD001","credit_history","total_debt","Total debt cannot be negative")

    # Summarize
    overall_status = ("NEEDS_REVIEW" if failed > 0 else "PASS")

    return ValidationReport(customer_id=customer_id,total_checks=total_checks,passed=passed,failed=failed,overall_status=overall_status,issues=issues)