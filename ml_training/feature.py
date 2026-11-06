import pandas as pd

df = pd.read_csv("credigo_credit_default_dataset.csv")

# 1. แยกกลุ่ม Default และ Non-default
print("Average Feature Values by Default Flag")

print(
    df.groupby("default_flag")[
        [
            "customer_age",
            "monthly_income",
            "total_debt",
            "credit_score",
            "credit_utilization",
            "debt_to_income_ratio",
            "late_payment_count",
            "max_days_past_due",
            "previous_default_count",
            "repayment_ratio"
        ]
    ].mean().round(2)
)

# 2. วิเคราะห์ Default Rate ตามประเภทอาชีพ
print("\nDefault Rate by Employment Type")

print(df.groupby("employment_type")["default_flag"].mean().mul(100).round(2))

# 3. วิเคราะห์ Default Rate ตามประเภทสินเชื่อ
print("\nDefault Rate by Loan Type")

print(df.groupby("loan_type")["default_flag"].mean().mul(100).round(2))