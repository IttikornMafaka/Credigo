
from backend.schemas.credit_risk_report import (
    CreditRiskReport
)

from backend.services.report_validator import (
    validate_overall_risk_level
)


# Create sample LLM report
report = CreditRiskReport(
    recommendation="manual_review_required",
    risk_level="LOW",
    executive_summary="Test report",
    key_risk_factors=[],
    verified_findings=[],
    missing_information=[],
    limitations=[]
)


# Simulate incomplete evidence
evidence_context = {
    "evidence": {
        "passed": [],
        "failed": [],
        "unverified": [
            {
                "policy_id": "CRP-031",
                "check_id": "debt_to_income_ratio",
                "status": "UNVERIFIED"
            }
        ],
        "not_required": []
    }
}


validated_report = validate_overall_risk_level(
    report,
    evidence_context
)

print("Original Risk Level:")
print(report.risk_level)

print("\nValidated Risk Level:")
print(validated_report.risk_level)

assert validated_report.risk_level == "UNKNOWN"

print("\nOverall Risk Level Validator Test PASSED")
