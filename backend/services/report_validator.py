
from backend.schemas.credit_risk_report import CreditRiskReport


# Approved severity mapping
# Add policy mappings only after confirming authoritative criteria.

APPROVED_SEVERITY_MAPPING = {
    # Example:
    # ("CRP-XXX", "some_check", "FAIL"): "HIGH"
}


def validate_recommendation(
    report: CreditRiskReport,
    evidence_context: dict
) -> CreditRiskReport:

    # 1. Get evidence groups
    evidence_groups = evidence_context.get(
        "evidence", {}
    )

    failed_evidence = evidence_groups.get(
        "failed", []
    )

    unverified_evidence = evidence_groups.get(
        "unverified", []
    )

    # 2. Check whether manual review is required
    manual_review_required = (
        evidence_context.get(
            "manual_review_required", False
        )
        or len(failed_evidence) > 0
        or len(unverified_evidence) > 0
    )

    # 3. Enforce recommendation
    if manual_review_required:

        report = report.model_copy(
            update={
                "recommendation": "manual_review_required"
            }
        )

    # 4. Return validated report
    return report


def validate_evidence_references(
    report: CreditRiskReport,
    evidence_context: dict
) -> CreditRiskReport:

    # 1. Collect all available evidence
    evidence_groups = evidence_context.get(
        "evidence", {}
    )

    available_evidence = []

    for group_name in [
        "passed",
        "failed",
        "unverified",
        "not_required"
    ]:
        available_evidence.extend(
            evidence_groups.get(group_name, [])
        )

    # 2. Validate every evidence reference
    for risk_factor in report.key_risk_factors:

        for reference in risk_factor.evidence:

            matched = False

            for item in available_evidence:

                same_policy = (
                    reference.policy_id
                    == item.get("policy_id")
                )

                same_check = (
                    reference.check_id
                    == item.get("check_id")
                )

                same_status = (
                    reference.status
                    == item.get("status")
                )

                same_source = (
                    reference.source is None
                    or reference.source == item.get("source")
                )

                if (
                    same_policy
                    and same_check
                    and same_status
                    and same_source
                ):
                    matched = True
                    break

            # 3. Reject unknown evidence
            if not matched:
                raise ValueError(
                    "Invalid Evidence Reference: "
                    f"{reference.policy_id} / "
                    f"{reference.check_id}"
                )

    return report


def validate_risk_severity(
    report: CreditRiskReport
) -> CreditRiskReport:

    validated_factors = []

    for risk_factor in report.key_risk_factors:

        # 1. Find approved severity for each evidence
        approved_severities = []

        for reference in risk_factor.evidence:

            mapping_key = (
                reference.policy_id,
                reference.check_id,
                reference.status
            )

            approved_severity = (
                APPROVED_SEVERITY_MAPPING.get(
                    mapping_key
                )
            )

            if approved_severity is None:
                approved_severities.append("UNKNOWN")

            else:
                approved_severities.append(
                    approved_severity
                )

        # 2. Determine validated severity
        if (
            not approved_severities
            or "UNKNOWN" in approved_severities
            or len(set(approved_severities)) != 1
        ):
            final_severity = "UNKNOWN"

        else:
            final_severity = approved_severities[0]

        # 3. Replace LLM severity with approved severity
        validated_factor = risk_factor.model_copy(
            update={
                "severity": final_severity
            }
        )

        validated_factors.append(
            validated_factor
        )

    # 4. Return updated report
    return report.model_copy(
        update={
            "key_risk_factors": validated_factors
        }
    )


def validate_overall_risk_level(
    report: CreditRiskReport,
    evidence_context: dict
) -> CreditRiskReport:

    # 1. Get evidence groups
    evidence_groups = evidence_context.get(
        "evidence", {}
    )

    failed_evidence = evidence_groups.get(
        "failed", []
    )

    unverified_evidence = evidence_groups.get(
        "unverified", []
    )

    # 2. Check evidence completeness
    has_incomplete_evidence = (
        len(failed_evidence) > 0
        or len(unverified_evidence) > 0
    )

    # 3. No approved overall risk calculation
    # is available yet.
    if has_incomplete_evidence:
        final_risk_level = "UNKNOWN"
    else:
        final_risk_level = "UNKNOWN"

    # 4. Replace LLM overall risk level
    return report.model_copy(
        update={
            "risk_level": final_risk_level
        }
    )


def validate_credit_risk_report(
    report: CreditRiskReport,
    evidence_context: dict
) -> CreditRiskReport:

    # 1. Validate Evidence References
    report = validate_evidence_references(
        report=report,
        evidence_context=evidence_context
    )

    # 2. Validate Recommendation
    report = validate_recommendation(
        report=report,
        evidence_context=evidence_context
    )

    # 3. Validate Risk Severity
    report = validate_risk_severity(
        report=report
    )

    # 4. Validate Overall Risk Level
    report = validate_overall_risk_level(
        report=report,
        evidence_context=evidence_context
    )

    return report
