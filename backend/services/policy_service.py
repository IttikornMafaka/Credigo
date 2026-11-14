from uuid import UUID
from datetime import date 
from sqlalchemy.orm import Session

from app.model.session import Customer,Employment,LoanApplication,Repayment

def check_crp_015(db: Session, national_id: str, application_id: UUID):
    
    # 1. Find customer
    customer = (
        db.query(Customer)
        .filter(Customer.national_id == national_id)
        .first()
    )

    if not customer:
        raise ValueError("Customer not found")

    # 2. Find loan application
    application = (
        db.query(LoanApplication)
        .filter(
            LoanApplication.application_id == application_id,
            LoanApplication.customer_id == customer.customer_id
        )
        .first()
    )

    if not application:
        raise ValueError("Loan application not found")

    # 3. Find latest employment record
    employment = (
        db.query(Employment)
        .filter(
            Employment.customer_id == customer.customer_id
        )
        .order_by(Employment.employment_start_date.desc())
        .first()
    )

    # 4. Extract application data
    requested_amount = float(application.requested_amount)
    requested_term = application.requested_term_months

    # 5. Prepare policy results
    results = []
    
        # 6. Check minimum loan amount
    results.append({
        "rule": "CRP-015",
        "check": "minimum_loan_amount",
        "status": "PASS" if requested_amount >= 1000 else "FAIL",
        "actual": requested_amount,
        "required": ">= 1000 HCU",
        "reason": (
            "Requested loan amount meets the minimum requirement."
            if requested_amount >= 1000
            else "Requested loan amount is below the minimum requirement."
        ),
        "source": "loan_applications.requested_amount"
    })

    # 7. Check maximum loan amount
    results.append({
        "rule": "CRP-015",
        "check": "maximum_loan_amount",
        "status": "PASS" if requested_amount <= 50000 else "FAIL",
        "actual": requested_amount,
        "required": "<= 50000 HCU",
        "reason": (
            "Requested loan amount is within the maximum limit."
            if requested_amount <= 50000
            else "Requested loan amount exceeds the maximum limit."
        ),
        "source": "loan_applications.requested_amount"
    })

    # 8. Check loan term
    results.append({
        "rule": "CRP-015",
        "check": "loan_term",
        "status": "PASS" if 6 <= requested_term <= 60 else "FAIL",
        "actual": requested_term,
        "required": "6-60 months",
        "reason": (
            "Requested loan term is within the allowed range."
            if 6 <= requested_term <= 60
            else "Requested loan term is outside the allowed range."
        ),
        "source": "loan_applications.requested_term_months"
    })

    # 9. Check income-based loan limit
    if employment and employment.monthly_income is not None:

        annual_income = float(employment.monthly_income) * 12
        max_loan_amount = annual_income * 0.60

        income_check_passed = requested_amount <= max_loan_amount

        results.append({
            "rule": "CRP-015",
            "check": "income_based_loan_limit",
            "status": "PASS" if income_check_passed else "FAIL",
            "actual": requested_amount,
            "required": max_loan_amount,
            "annual_income": annual_income,
            "reason": (
                "Requested loan amount is within the income-based limit."
                if income_check_passed
                else "Requested loan amount exceeds the income-based limit."
            ),
            "source": "employment_records.monthly_income"
        })

    else:
        results.append({
            "rule": "CRP-015",
            "check": "income_based_loan_limit",
            "status": "UNVERIFIED",
            "reason": "Monthly income evidence is unavailable.",
            "source": "employment_records.monthly_income"
        })

    # 10. Check senior officer review
    senior_review_required = requested_amount > 25000

    results.append({
        "rule": "CRP-015",
        "check": "senior_officer_review",
        "status": "REQUIRED" if senior_review_required else "NOT_REQUIRED",
        "actual": requested_amount,
        "threshold": 25000,
        "reason": (
            "Senior officer review is required."
            if senior_review_required
            else "Senior officer review is not required."
        ),
        "source": "CRP-015 policy threshold"
    })

    # 11. Return result
    return {
        "application_id": str(application.application_id),
        "customer_id": str(customer.customer_id),
        "policy": "CRP-015",
        "results": results
    }
    
    
def get_crp_041_evidence(
    db: Session,
    national_id: str
):
    # 1. Find customer
    customer = (
        db.query(Customer)
        .filter(Customer.national_id == national_id)
        .first()
    )

    if not customer:
        raise ValueError("Customer not found")

    # 2. Calculate 24-month lookback date
    today = date.today()

    try:
        cutoff_date = date(
            today.year - 2,
            today.month,
            today.day
        )
    except ValueError:
        # Handle February 29 in a leap year
        cutoff_date = date(
            today.year - 2,
            today.month,
            28
        )

    # 3. Retrieve repayment records
    repayments = (
        db.query(Repayment)
        .filter(
            Repayment.customer_id == customer.customer_id,
            Repayment.due_date >= cutoff_date,
            Repayment.due_date <= today
        )
        .order_by(Repayment.due_date.asc())
        .all()
    )

    # 4. Prepare evidence
    repayment_evidence = []

    late_count = 0
    missed_count = 0
    paid_late_count = 0 
    max_dpd = 0
    data_quality_issues = []

    for repayment in repayments:

        status = repayment.payment_status.strip().lower()

        if status == "late":
            late_count += 1

        elif status == "missed":
            missed_count += 1

        # Calculate DPD
        if status in ["paid", "late"]:

            if repayment.payment_date is None:
                data_quality_issues.append(
                    f"Repayment {repayment.repayment_id}: "
                    "Missing payment_date"
                )
                dpd = None

            else:
                dpd = max(
                    (repayment.payment_date - repayment.due_date).days,
                    0
                )

                if status == "late" and dpd == 0:
                    data_quality_issues.append(
                        f"Repayment {repayment.repayment_id}: "
                        "Late status conflicts with payment_date"
                    )

        elif status == "missed":

            if repayment.payment_date is not None:
                data_quality_issues.append(
                    f"Repayment {repayment.repayment_id}: "
                    "Missed status conflicts with payment_date"
                )
                dpd = None

            else:
                dpd = max(
                    (today - repayment.due_date).days,
                    0
                )

        else:
            data_quality_issues.append(
                f"Repayment {repayment.repayment_id}: "
                f"Unsupported status: {repayment.payment_status}"
            )
            dpd = None

        if dpd is not None:
            max_dpd = max(max_dpd, dpd)
            if status == "paid" and dpd > 0:
                paid_late_count += 1

        repayment_evidence.append({
            "repayment_id": repayment.repayment_id,
            "due_date": repayment.due_date.isoformat(),
            "payment_date": (
                repayment.payment_date.isoformat()
                if repayment.payment_date
                else None
            ),
            "payment_status": repayment.payment_status,
            "dpd": dpd
        })

    # 5. Determine evidence quality
    if not repayments:
        evidence_status = "UNVERIFIED"

    elif data_quality_issues:
        evidence_status = "UNVERIFIED"

    else:
        evidence_status = "READY_FOR_POLICY_CHECK"

    return {
        "customer_id": str(customer.customer_id),
        "policy": "CRP-041",
        "lookback_months": 24,
        "cutoff_date": cutoff_date.isoformat(),
        "assessment_date": today.isoformat(),
        "evidence_status": evidence_status,
        "total_records": len(repayments),
        "late_count": late_count,
        "missed_count": missed_count,
        "max_dpd": max_dpd,
        "has_90_plus_dpd": max_dpd >= 90,
        "data_quality_issues": data_quality_issues,
        "repayments": repayment_evidence ,
        "paid_late_count": paid_late_count 
    }
    
def check_crp_041(
    db: Session,
    national_id: str
):
    # 1. Retrieve repayment evidence
    evidence = get_crp_041_evidence(
        db=db,
        national_id=national_id
    )

    # 2. Check evidence quality
    if evidence["evidence_status"] != "READY_FOR_POLICY_CHECK":
        status = "UNVERIFIED"
        reason = "Repayment evidence is incomplete or unavailable."

    # 3. Check 90+ DPD condition
    elif evidence["has_90_plus_dpd"]:
        status = "FAIL"
        reason = "Repayment with 90 or more days past due was detected."

    # 4. No 90+ DPD detected
    else:
        status = "PASS"
        reason = "No repayment with 90 or more days past due was detected."

    return {
        "customer_id": evidence["customer_id"],
        "policy": "CRP-041",
        "check": "repayment_history",
        "status": status,
        "reason": reason,
        "evidence": {
            "lookback_months": evidence["lookback_months"],
            "total_records": evidence["total_records"],
            "late_count": evidence["late_count"],
            "missed_count": evidence["missed_count"],
            "paid_late_count": evidence["paid_late_count"],
            "max_dpd": evidence["max_dpd"],
            "has_90_plus_dpd": evidence["has_90_plus_dpd"],
            "data_quality_issues": evidence["data_quality_issues"]
        },
        "source":"repayment_records"
    }
    
def check_crp_031(db: Session,national_id: str,application_id: UUID):
    # 1. Find customer
    customer = (
        db.query(Customer)
        .filter(Customer.national_id == national_id)
        .first()
    )

    if not customer:
        raise ValueError("Customer not found")

    # 2. Find loan application
    application = (
        db.query(LoanApplication)
        .filter(
            LoanApplication.application_id == application_id,
            LoanApplication.customer_id == customer.customer_id
        )
        .first()
    )

    if not application:
        raise ValueError("Loan application not found")

    # 3. Monthly debt installment is unavailable
    return {
        "application_id": str(application.application_id),
        "customer_id": str(customer.customer_id),
        "policy": "CRP-031",
        "check": "debt_to_income_ratio",
        "status": "UNVERIFIED",
        "reason": (
            "Monthly debt installment information is unavailable. "
            "Outstanding debt balance cannot be used as a substitute "
            "for monthly debt obligations."
        ),
        "source": (
        "Credit.total_debt "
        "(outstanding balance only; "
        "monthly installment unavailable)"
            )
    }


def check_crp_010(db: Session, national_id: str):

    # 1. Find customer
    customer = (
        db.query(Customer)
        .filter(Customer.national_id == national_id)
        .first()
    )

    if not customer:
        return {
            "customer_id": None,
            "policy": "CRP-010",
            "status": "FAIL",
            "reason": "Customer record not found.",
            "evidence": {}
        }

    # 2. Validate National ID
    national_id_valid = (
        customer.national_id is not None
        and len(customer.national_id) == 13
        and customer.national_id.isdigit()
    )

    # 3. Validate personal information
    first_name_valid = bool(
        customer.first_name and customer.first_name.strip()
    )

    last_name_valid = bool(
        customer.last_name and customer.last_name.strip()
    )

    dob_valid = (
        customer.date_of_birth is not None
        and customer.date_of_birth <= date.today()
    )

    # 4. Optional contact information
    phone_provided = bool(
        customer.phone_number and customer.phone_number.strip()
    )

    email_provided = bool(
        customer.email and customer.email.strip()
    )

    address_provided = bool(
        customer.address and customer.address.strip()
    )

    # 5. Collect results
    checks = {
        "national_id": national_id_valid,
        "first_name": first_name_valid,
        "last_name": last_name_valid,
        "date_of_birth": dob_valid,
        "phone_number_provided": phone_provided,
        "email_provided": email_provided,
        "address_provided": address_provided
    }

    required_checks = [
        national_id_valid,
        first_name_valid,
        last_name_valid,
        dob_valid
    ]

    basic_data_status = (
        "PASS" if all(required_checks) else "FAIL"
    )

    return {
        "customer_id": str(customer.customer_id),
        "policy": "CRP-010",
        "status": "UNVERIFIED",
        "basic_data_status": basic_data_status,
        "reason": (
            "Basic customer data is valid, but identity "
            "verification and KYC evidence are not available."
        ),
        "evidence": checks, 
        "check": "identity_verification",
        "source": "customers_detail",
    }


def normalize_policy_result(item: dict) -> dict:
    
    known_fields = {
        "rule",
        "policy",
        "check",
        "status",
        "reason",
        "actual",
        "required",
        "threshold",
        "source"
    }

    details = {
        key: value
        for key, value in item.items()
        if key not in known_fields
        and key not in {"application_id", "customer_id"}
    }

    return {
        "policy_id": item.get("policy") or item.get("rule"),
        "check_id": item.get("check"),
        "status": item.get("status"),
        "reason": item.get("reason"),
        "observed_value": item.get("actual"),
        "expected_value": (
            item.get("required")
            if "required" in item
            else item.get("threshold")
        ),
        "source": item.get("source"),
        "details": details
    }


def run_policy_assessment(db: Session,national_id: str,application_id: UUID):
    # 1. Run all policies
    crp_015 = check_crp_015(db=db,national_id=national_id,application_id=application_id)
    crp_031 = check_crp_031(db=db,national_id=national_id,application_id=application_id)
    crp_041 = check_crp_041(db=db,national_id=national_id)
    crp_010 = check_crp_010(db=db,national_id=national_id)

    # 2. Combine all policy results
    all_results = (crp_015["results"] + [crp_031]+ [crp_041]+ [crp_010])

    # 3. Determine overall assessment status
    statuses = [item["status"] for item in all_results]
    
    evidence_records = [normalize_policy_result(item)for item in all_results]

    if "FAIL" in statuses:
        assessment_status = "FAIL"

    elif "UNVERIFIED" in statuses:
        assessment_status = "UNVERIFIED"

    else:
        assessment_status = "PASS"

    # 4. Check senior officer review
    senior_review_required = any(
        item.get("status") == "REQUIRED"
        for item in all_results
    )

    # 5. Identify reasons for manual review
    review_reasons = []

    if senior_review_required:
        review_reasons.append("SENIOR_OFFICER_REVIEW")

    if "FAIL" in statuses:
        review_reasons.append("POLICY_FAILURE")

    if "UNVERIFIED" in statuses:
        review_reasons.append("UNVERIFIED_EVIDENCE")

    manual_review_required = len(review_reasons) > 0

    # 6. Policy summary
    policy_summary = {
        "total_checks": len(all_results),
        "passed": statuses.count("PASS"),
        "failed": statuses.count("FAIL"),
        "unverified": statuses.count("UNVERIFIED"),
        "not_required": statuses.count("NOT_REQUIRED"),
        "senior_review_required": senior_review_required,
        "manual_review_required": manual_review_required
    }

    # 7. Return assessment
    return {
        "application_id": str(application_id),
        "customer_id": crp_015["customer_id"],
        "assessment_status": assessment_status,
        "senior_review_required": senior_review_required,
        "manual_review_required": manual_review_required,
        "review_reasons": review_reasons,
        "policy_summary": policy_summary,
        "evidence_records": evidence_records,
        "policy_results": all_results, 
    }