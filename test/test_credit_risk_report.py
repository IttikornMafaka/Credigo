
from backend.schemas.credit_risk_report import CreditRiskReport


report_data = {
    "recommendation": "manual_review_required",
    "risk_level": "UNKNOWN",

    "executive_summary": (
        "The application meets the configured loan amount "
        "and loan term checks. However, DTI and KYC evidence "
        "remain unverified."
    ),

    "key_risk_factors": [
        {
            "factor": "Debt-to-Income Ratio",
            "explanation": (
                "Monthly debt installment information is unavailable."
            ),
            "severity": "UNKNOWN",
            "evidence": [
                {
                    "policy_id": "CRP-031",
                    "check_id": "debt_to_income_ratio",
                    "status": "UNVERIFIED",
                    "source": "Credit.total_debt"
                }
            ]
        }
    ],

    "verified_findings": [
        "Requested loan amount meets the configured limits.",
        "Requested loan term is within the configured range."
    ],

    "missing_information": [
        "Monthly debt installment information.",
        "Verified KYC documentation."
    ],

    "limitations": [
        "The final lending decision must be made by an authorized human officer."
    ]
}


report = CreditRiskReport(**report_data)

print("\n--- CREDIT RISK REPORT ---")
print(report.model_dump_json(indent=2))

print("\n--- VALIDATION RESULT ---")
print("Pydantic validation successful!")
