import pandas as pd

from backend.services.prediction_service import predict_credit_risk

customer_data = pd.DataFrame([{
    "customer_age": 30,
    "gender": "Male",
    "marital_status": "Single",
    "education": "Bachelor",
    "employment_type": "Full-time",
    "monthly_income": 35000,
    "employment_tenure_months": 48,
    "total_account_balance": 80000,
    "total_debt": 120000,
    "credit_score": 650,
    "credit_utilization": 0.45,
    "debt_to_income_ratio": 0.35,
    "loan_amount": 200000,
    "loan_term_months": 36,
    "loan_purpose": "Personal",
    "loan_type": "Personal Loan",
    "previous_loan_count": 2,
    "late_payment_count": 1,
    "max_days_past_due": 15,
    "previous_default_count": 0,
    "repayment_ratio": 0.90
}])

result = predict_credit_risk(customer_data)

print("Prediction Result:")
print(result)