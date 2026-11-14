
from backend.schemas.credit_risk_report import (
    CreditRiskReport
)

from backend.services.report_validator import (
    validate_evidence_references
)


# 1. Create sample report
report = CreditRiskReport(
    recommendation="manual_review_required",
    risk_level="UNKNOWN",
    executive_summary="Test report",
    key_risk_factors=[
        {
            "factor": "Unverified DTI",
            "explanation": "Monthly debt installment is missing.",
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
    ]
)


# 2. Create evidence context
evidence_context = {
    "evidence": {
        "passed": [],
        "failed": [],
        "not_required": [],
        "unverified": [
            {
                "policy_id": "CRP-031",
                "check_id": "debt_to_income_ratio",
                "status": "UNVERIFIED",
                "source": "Credit.total_debt"
            }
        ]
    }
}


# 3. Validate
validated_report = validate_evidence_references(
    report,
    evidence_context
)

print("Evidence Reference Validation PASSED")


# 4. Test fake evidence
fake_context = {
    "evidence": {
        "passed": [],
        "failed": [],
        "unverified": [],
        "not_required": []
    }
}

try:
    validate_evidence_references(
        report,
        fake_context
    )

    raise AssertionError(
        "Validator should reject fake evidence"
    )

except ValueError as error:
    print("Fake Evidence Rejected")
    print(error)


print("\nAll Tests PASSED")
