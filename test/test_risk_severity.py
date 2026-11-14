
from backend.schemas.credit_risk_report import (
    CreditRiskReport
)

from backend.services.report_validator import (
    validate_risk_severity
)


report = CreditRiskReport(
    recommendation="manual_review_required",
    risk_level="HIGH",
    executive_summary="Test report",
    key_risk_factors=[
        {
            "factor": "Unverified DTI",
            "explanation": "Monthly debt installment is missing.",
            "severity": "HIGH",
            "evidence": [
                {
                    "policy_id": "CRP-031",
                    "check_id": "debt_to_income_ratio",
                    "status": "UNVERIFIED",
                    "source": "Credit.total_debt"
                }
            ]
        }
    ]
)


# Run Validator
validated_report = validate_risk_severity(report)


print("Original Severity:")
print(report.key_risk_factors[0].severity)

print("\nValidated Severity:")
print(validated_report.key_risk_factors[0].severity)


assert (
    validated_report.key_risk_factors[0].severity
    == "UNKNOWN"
)

print("\nRisk Severity Validator Test PASSED")
