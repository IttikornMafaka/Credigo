
from unittest.mock import patch, MagicMock

import agent.nodes as nodes
from backend.schemas.credit_risk_report import CreditRiskReport


# Mock Report สำหรับใช้ทดสอบ
def create_mock_report():

    return CreditRiskReport(
        recommendation="manual_review_required",
        risk_level="UNKNOWN",
        executive_summary="Some evidence requires manual review.",
        key_risk_factors=[],
        verified_findings=[],
        missing_information=["DTI verification"],
        limitations=["KYC verification is unavailable"]
    )


# Test 1: Policy Assessment Node
def test_policy_assessment_node():

    fake_assessment = {
        "assessment_status": "NEEDS_REVIEW",
        "manual_review_required": True
    }

    fake_db = MagicMock()

    with patch.object(nodes, "SessionLocal", return_value=fake_db):
        with patch.object(
            nodes,
            "run_policy_assessment",
            return_value=fake_assessment
        ) as mock_policy:

            result = nodes.policy_assessment_node({
                "customer_data": {
                    "national_id": "TEST_NATIONAL_ID"
                },
                "application_id": "TEST_APPLICATION_ID"
            })

    assert result["status"] == "policy_assessment_completed"
    assert result["policy_assessment"] == fake_assessment

    mock_policy.assert_called_once()
    fake_db.close.assert_called_once()


# Test 2: Evidence Builder Node
def test_evidence_builder_node():

    fake_assessment = {
        "assessment_status": "NEEDS_REVIEW"
    }

    fake_context = {
        "manual_review_required": True,
        "evidence": {
            "passed": [],
            "failed": [],
            "unverified": [],
            "not_required": []
        }
    }

    with patch.object(
        nodes,
        "build_evidence_context",
        return_value=fake_context
    ) as mock_builder:

        result = nodes.evidence_builder_node({
            "policy_assessment": fake_assessment
        })

    assert result["status"] == "evidence_context_created"
    assert result["evidence_context"] == fake_context

    mock_builder.assert_called_once_with(fake_assessment)


# Test 3: Credit Risk Report Node
def test_credit_risk_report_node():

    fake_context = {
        "manual_review_required": True,
        "evidence": {
            "passed": [],
            "failed": [],
            "unverified": [],
            "not_required": []
        }
    }

    fake_report = create_mock_report()

    with patch.object(
        nodes,
        "generate_credit_risk_report",
        return_value=fake_report
    ) as mock_llm:

        result = nodes.credit_risk_report_node({
            "evidence_context": fake_context
        })

    assert result["status"] == "credit_risk_report_completed"

    assert (
        result["credit_risk_report"]["recommendation"]
        == "manual_review_required"
    )

    mock_llm.assert_called_once_with(
        evidence_context=fake_context
    )


# Test 4: Report Validation Node
def test_report_validation_node():

    fake_context = {
        "manual_review_required": True,
        "evidence": {
            "passed": [],
            "failed": [],
            "unverified": [],
            "not_required": []
        }
    }

    fake_report = create_mock_report()

    report_data = fake_report.model_dump(mode="json")

    with patch.object(
        nodes,
        "validate_credit_risk_report",
        return_value=fake_report
    ) as mock_validator:

        result = nodes.report_validation_node({
            "credit_risk_report": report_data,
            "evidence_context": fake_context
        })

    assert result["status"] == "report_validation_completed"

    assert (
        result["ai_recommend"]
        == "manual_review_required"
    )

    mock_validator.assert_called_once()


# Failure Test 1: Missing Customer Data
def test_policy_assessment_missing_customer():

    result = nodes.policy_assessment_node({
        "customer_data": {},
        "application_id": "TEST_APPLICATION_ID"
    })

    assert result["status"] == "policy_assessment_failed"
    assert "error" in result


# Failure Test 2: Missing Evidence
def test_evidence_builder_missing_assessment():

    result = nodes.evidence_builder_node({})

    assert result["status"] == "evidence_build_failed"


# Failure Test 3: Missing Evidence Context
def test_credit_risk_report_missing_context():

    result = nodes.credit_risk_report_node({})

    assert result["status"] == "credit_risk_report_failed"


# Failure Test 4: Missing Report
def test_report_validation_missing_report():

    result = nodes.report_validation_node({
        "evidence_context": {
            "evidence": {
                "passed": [],
                "failed": [],
                "unverified": [],
                "not_required": []
            }
        }
    })

    assert result["status"] == "report_validation_failed"
    assert result["ai_recommend"] == "manual_review_required"


# Failure Test 5: LLM Error
def test_credit_risk_report_llm_error():

    fake_context = {
        "manual_review_required": True,
        "evidence": {
            "passed": [],
            "failed": [],
            "unverified": [],
            "not_required": []
        }
    }

    with patch.object(
        nodes,
        "generate_credit_risk_report",
        side_effect=Exception("Mock LLM Error")
    ):

        result = nodes.credit_risk_report_node({
            "evidence_context": fake_context
        })

    assert result["status"] == "credit_risk_report_failed"
    assert "Mock LLM Error" in result["error"]

