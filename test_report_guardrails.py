
from backend.schemas.credit_risk_report import (
    CreditRiskReport,
    RiskFactor,
    EvidenceReference
)

from backend.services.report_validator import (
    validate_credit_risk_report
)
# 1. จำลอง Evidence Context
evidence_context = {
    "manual_review_required": True,

    "evidence": {
        "passed": [],

        "failed": [],

        "unverified": [
            {
                "policy_id": "CRP-031",
                "check_id": "debt_to_income_ratio",
                "status": "UNVERIFIED",
                "reason": "Monthly debt installment is unavailable.",
                "source": (
                    "Credit.total_debt "
                    "(outstanding balance only; "
                    "monthly installment unavailable)"
                ),
                "observed_value": None,
                "expected_value": None,
                "details": {
                    "monthly_debt_installment": None
                }
            }
        ],

        "not_required": []
    }
}


# 2. จำลองว่า LLM แนะนำอนุมัติ
fake_report = CreditRiskReport(
    recommendation="recommend_approval",
    risk_level="LOW",
    executive_summary="The applicant is low risk.",
    key_risk_factors=[
        RiskFactor(
            factor="Debt-to-Income Ratio",
            explanation="DTI is unavailable.",
            severity="HIGH",
            evidence=[
                EvidenceReference(
                    policy_id="CRP-031",
                    check_id="debt_to_income_ratio",
                    status="UNVERIFIED",
                    source="Credit.total_debt (outstanding balance only; monthly installment unavailable)"
                )
            ]
        )
    ],
    verified_findings=[],
    missing_information=["Monthly debt installment"],
    limitations=[]
)


# 3. ส่งเข้า Python Guardrails
validated_report = validate_credit_risk_report(
    fake_report,
    evidence_context
)


# 4. ตรวจสอบผล
print("\n--- GUARDRAIL TEST ---")

print("Recommendation:", validated_report.recommendation)
print("Risk Level:", validated_report.risk_level)

print(
    "Risk Factor Severity:",
    validated_report.key_risk_factors[0].severity
)

assert validated_report.recommendation == "manual_review_required"
assert validated_report.risk_level == "UNKNOWN"
assert validated_report.key_risk_factors[0].severity == "UNKNOWN"

print("\nALL GUARDRAIL TESTS PASSED")

# 5. Test Fake Evidence
print("\n--- FAKE EVIDENCE TEST ---")

fake_reference = fake_report.key_risk_factors[0].evidence[0].model_copy(
    update={
        "policy_id": "CRP-999"
    }
)

fake_factor = fake_report.key_risk_factors[0].model_copy(
    update={
        "evidence": [fake_reference]
    }
)

fake_evidence_report = fake_report.model_copy(
    update={
        "key_risk_factors": [fake_factor]
    }
)

try:
    validate_credit_risk_report(
        fake_evidence_report,
        evidence_context
    )

    raise AssertionError("Fake Evidence was not rejected!")

except ValueError as error:
    print("Fake Evidence Rejected:", error)

print("FAKE EVIDENCE TEST PASSED")


# 6. Test UNVERIFIED -> PASS manipulation
print("\n--- EVIDENCE STATUS MANIPULATION TEST ---")

fake_status_reference = fake_report.key_risk_factors[0].evidence[0].model_copy(
    update={
        "status": "PASS"
    }
)

fake_status_factor = fake_report.key_risk_factors[0].model_copy(
    update={
        "evidence": [fake_status_reference]
    }
)

fake_status_report = fake_report.model_copy(
    update={
        "key_risk_factors": [fake_status_factor]
    }
)

try:
    validate_credit_risk_report(
        fake_status_report,
        evidence_context
    )

    raise AssertionError("Fake PASS status was not rejected!")

except ValueError as error:
    print("Fake PASS Status Rejected:", error)

print("STATUS MANIPULATION TEST PASSED")