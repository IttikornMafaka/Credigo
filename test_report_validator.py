
from backend.services.report_validator import (
    validate_recommendation
)

from backend.schemas.credit_risk_report import (
    CreditRiskReport
)


# Simulate LLM report
report = CreditRiskReport(
    recommendation="recommend_approval",
    risk_level="LOW",
    executive_summary="Test report",
    key_risk_factors=[],
    verified_findings=[],
    missing_information=[],
    limitations=[]
)


# Simulate evidence context
evidence_context = {
    "manual_review_required": True,
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


# Run Validator
validated_report = validate_recommendation(
    report=report,
    evidence_context=evidence_context
)


print("Original Recommendation:")
print(report.recommendation)

print("\nValidated Recommendation:")
print(validated_report.recommendation)

assert (
    validated_report.recommendation
    == "manual_review_required"
)

print("\nReport Validator Test PASSED")
