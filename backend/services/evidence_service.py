
def build_evidence_context(assessment: dict) -> dict:
    """
    Prepare policy assessment evidence for LLM investigation.
    """

    evidence_records = assessment.get("evidence_records", [])

    passed_evidence = []
    failed_evidence = []
    unverified_evidence = []
    not_required_evidence = []

    for record in evidence_records:

        status = record.get("status")

        if status == "PASS":
            passed_evidence.append(record)

        elif status == "FAIL":
            failed_evidence.append(record)

        elif status == "UNVERIFIED":
            unverified_evidence.append(record)

        elif status == "NOT_REQUIRED":
            not_required_evidence.append(record)

    return {
        "application_id": assessment.get("application_id"),
        "customer_id": assessment.get("customer_id"),

        "assessment_status": assessment.get("assessment_status"),

        "manual_review_required": assessment.get(
            "manual_review_required"
        ),

        "review_reasons": assessment.get("review_reasons", []),

        "policy_summary": assessment.get("policy_summary", {}),

        "evidence": {
            "passed": passed_evidence,
            "failed": failed_evidence,
            "unverified": unverified_evidence,
            "not_required": not_required_evidence
        }
    }
