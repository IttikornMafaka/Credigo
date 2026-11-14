
from uuid import UUID
import os

from dotenv import load_dotenv

from backend.dependence.database import SessionLocal

from backend.services.policy_service import (
    run_policy_assessment
)

from backend.services.evidence_service import (
    build_evidence_context
)

from backend.services.llm_service import (
    generate_credit_risk_report
)


load_dotenv()

# 1. Check API Key
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY is missing")


# 2. Prepare database session
db = SessionLocal()

try:

    # Replace with the same test values
    # used in test_evidence_service.py
    national_id = "1101700000081"
    application_id = UUID("140ca4ca-87b0-43bc-8ff2-2196c03ace1d")

    # 3. Run Policy Assessment
    assessment = run_policy_assessment(
        db=db,
        national_id=national_id,
        application_id=application_id
    )

    print("\n--- POLICY ASSESSMENT COMPLETED ---")

    # 4. Build Evidence Context
    evidence_context = build_evidence_context(
        assessment
    )

    print("\n--- EVIDENCE CONTEXT CREATED ---")

    # 5. Call GPT-4.1-mini
    report = generate_credit_risk_report(
        evidence_context=evidence_context
    )

    # 6. Display LLM Report
    print("\n--- CREDIGO AI CREDIT RISK REPORT ---")

    print(report.model_dump_json(indent=2))

    # 7. Display Recommendation
    print("\n--- AI RECOMMENDATION ---")

    print(report.recommendation)

    print("\n--- RISK LEVEL ---")

    print(report.risk_level)

finally:
    db.close()
