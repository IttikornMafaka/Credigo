from unittest.mock import patch, MagicMock
from types import SimpleNamespace
from uuid import uuid4

from agent.graph import graph
from agent import nodes
from agent.schemas import CreditAnalysisResult, ReflectionResult
from backend.schemas.credit_risk_report import CreditRiskReport


def test_full_credit_risk_workflow():

    # ------------------------------------------------
    # 1. Prepare Mock IDs
    # ------------------------------------------------

    customer_id = uuid4()
    application_id = uuid4()

    # ------------------------------------------------
    # 2. Mock Customer
    # ------------------------------------------------

    fake_customer = SimpleNamespace(
        customer_id=customer_id,
        national_id="1234567890123"
    )

    # ------------------------------------------------
    # 3. Mock Validation Result
    # ------------------------------------------------

    fake_validation = MagicMock()

    fake_validation.overall_status = "PASS"
    fake_validation.total_checks = 5
    fake_validation.passed = 5
    fake_validation.failed = 0
    fake_validation.issues = []

    fake_validation.model_dump.return_value = {
        "overall_status": "PASS",
        "total_checks": 5,
        "passed": 5,
        "failed": 0,
        "issues": []
    }

    # ------------------------------------------------
    # 4. Mock RAG Documents
    # ------------------------------------------------

    fake_document = SimpleNamespace(
        metadata={
            "source": "mock_credit_policy.pdf",
            "page": 1
        },
        page_content="Mock credit policy content."
    )

    # ------------------------------------------------
    # 5. Mock Analysis Result
    # ------------------------------------------------

    fake_analysis = CreditAnalysisResult(
        risk_level="low",
        risk_factors=["No major risk identified in mock data."],
        policy_compliance=["Mock policy reviewed."],
        supporting_evidence=["Mock evidence reference."],
        recommendation="manual_review_required",
        reasoning_summary="Mock analysis based on test evidence."
    )

    # ------------------------------------------------
    # 6. Mock Reflection Result
    # ------------------------------------------------

    fake_reflection = ReflectionResult(
        is_consistent=True,
        issues=[],
        missing_information=[],
        requires_manual_review=False,
        reasoning_summary="Mock reflection passed."
    )

    # ------------------------------------------------
    # 7. Mock Credit Risk Report
    # ------------------------------------------------

    fake_report = CreditRiskReport(
        recommendation="manual_review_required",
        risk_level="UNKNOWN",
        executive_summary="Mock credit risk report.",
        key_risk_factors=[],
        verified_findings=["Mock validation passed."],
        missing_information=["Real customer evidence is unavailable."],
        limitations=["This is a simulated test."]
    )

    # ------------------------------------------------
    # 8. Mock LLM
    # ------------------------------------------------

    fake_llm = MagicMock()

    fake_llm.with_structured_output.return_value.invoke.side_effect = [
        fake_analysis,
        fake_reflection
    ]

    # ------------------------------------------------
    # 9. Mock Evidence Context
    # ------------------------------------------------

    fake_evidence_context = {
        "manual_review_required": True,
        "evidence": {
            "passed": [],
            "failed": [],
            "unverified": [],
            "not_required": []
        }
    }

    # ------------------------------------------------
    # 10. Mock Database and External Services
    # ------------------------------------------------

    with (
        patch.object(nodes, "SessionLocal") as mock_session,
        patch.object(
            nodes.customers_service,
            "get_customer_by_id",
            return_value=fake_customer
        ),
        patch.object(
            nodes,
            "validation_data",
            return_value=fake_validation
        ),
        patch.object(
            nodes,
            "predict_credit_risk",
            return_value={
                "prediction": "low_risk",
                "default_probability": 0.18,
                "risk_score": 20,
                "model_version": "mock_model"
            }
        ),
        patch.object(
            nodes,
            "search_policy",
            return_value=[fake_document]
        ),
        patch.object(
            nodes,
            "get_llm",
            return_value=fake_llm
        ),
        patch.object(
            nodes,
            "run_policy_assessment",
            return_value={"assessment_status": "completed"}
        ),
        patch.object(
            nodes,
            "build_evidence_context",
            return_value=fake_evidence_context
        ),
        patch.object(
            nodes,
            "generate_credit_risk_report",
            return_value=fake_report
        ),
        patch.object(
            nodes,
            "validate_credit_risk_report",
            side_effect=lambda report, evidence_context: report
        )
    ):

        # Mock Database Session
        fake_db = MagicMock()
        mock_session.return_value = fake_db

        # ------------------------------------------------
        # 11. Run Actual LangGraph
        # ------------------------------------------------

        initial_state = {
            "customer_id": customer_id,
            "application_id": application_id,
            "retry_count": 0,
            "max_retries": 2
        }

        result = graph.invoke(initial_state)

    # ------------------------------------------------
    # 12. Verify Final Result
    # ------------------------------------------------

    assert result["status"] == "report_validation_completed"

    assert result["credit_risk_report"]["recommendation"] == (
        "manual_review_required"
    )

    assert result["ai_recommend"] == "manual_review_required"

    assert result["customer_data"]["national_id"] == "1234567890123"

    assert "policy_assessment" in result
    assert "evidence_context" in result
    assert "credit_risk_report" in result

    # Confirm Database Session Was Closed
    assert fake_db.close.call_count >= 1

    # Confirm LLM Was Called For Analysis And Reflection
    assert fake_llm.with_structured_output.call_count == 2

    print("\nFULL CREDIGO WORKFLOW TEST PASSED")