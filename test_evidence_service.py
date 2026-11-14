
from uuid import UUID

from backend.dependence.database import SessionLocal
from backend.services.policy_service import run_policy_assessment
from backend.services.evidence_service import build_evidence_context


db = SessionLocal()

try:
    assessment = run_policy_assessment(
        db=db,
        national_id="1101700000081",
        application_id=UUID("140ca4ca-87b0-43bc-8ff2-2196c03ace1d")
    )

    evidence_context = build_evidence_context(assessment)

    print("\n--- EVIDENCE CONTEXT ---")
    print(evidence_context)

    print("\n--- EVIDENCE SUMMARY ---")
    for status, records in evidence_context["evidence"].items():
        print(f"{status}: {len(records)}")

finally:
    db.close()
