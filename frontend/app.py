import streamlit as st
import pandas as pd
from datetime import date

from api.client import (
    check_health,
    run_investigation,
    ApiError,
    search_customer,
    get_customer,
    register_customer,
    get_customer_profile,
    create_employment,
    create_account,
    create_credit_history,
    create_loan,
    create_repayment,
    create_loan_application,
)

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Credigo | Credit Risk Intelligence",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==========================================
# 2. DESIGN TOKENS
# ==========================================

NAVY = "#0F1B2D"
NAVY_LIGHT = "#1C2E4A"
BLUE = "#2563EB"
BLUE_LIGHT = "#EFF4FF"
BG = "#F6F8FC"
CARD_BG = "#FFFFFF"
BORDER = "#E4E9F2"
TEXT = "#0F1B2D"
TEXT_MUTED = "#64748B"
SIDEBAR_MUTED = "#93A3B8"
SUCCESS = "#0F9D58"
SUCCESS_TEXT = "#0A7A44"
SUCCESS_BG = "#E8F7EF"
DANGER = "#D93025"
DANGER_BG = "#FDECEA"
WARN = "#B26A00"
WARN_BG = "#FFF7E6"


# ==========================================
# 3. CUSTOM CSS
# ==========================================

st.markdown(
    f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }}

        .stApp {{
            background: {BG};
        }}

        button:focus-visible,
        [role="button"]:focus-visible {{
            outline: 2px solid {BLUE};
            outline-offset: 2px;
        }}

        /* ---------- Sidebar ---------- */
        [data-testid="stSidebar"] {{
            background: {NAVY};
            border-right: 1px solid {NAVY_LIGHT};
        }}

        [data-testid="stSidebar"] * {{
            color: #E2E8F0;
        }}

        [data-testid="stSidebar"] hr {{
            border-color: {NAVY_LIGHT};
        }}

        .brand {{
            font-size: 22px;
            font-weight: 800;
            letter-spacing: 2.5px;
            color: #FFFFFF;
            padding: 4px 0 2px 0;
        }}

        .brand-sub {{
            font-size: 11px;
            font-weight: 500;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            color: {SIDEBAR_MUTED};
            margin-bottom: 4px;
        }}

        .sidebar-meta {{
            font-size: 11px;
            color: {SIDEBAR_MUTED};
            letter-spacing: 0.5px;
            line-height: 1.6;
        }}

        .sidebar-label {{
            font-size: 10.5px;
            font-weight: 700;
            letter-spacing: 1.8px;
            text-transform: uppercase;
            color: {SIDEBAR_MUTED};
            margin-bottom: 8px;
        }}

        .sidebar-chip {{
            background: {NAVY_LIGHT};
            border: 1px solid #2B3F60;
            border-radius: 10px;
            padding: 10px 12px;
            margin-bottom: 8px;
        }}

        .sidebar-chip-label {{
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 1.2px;
            text-transform: uppercase;
            color: {SIDEBAR_MUTED};
            margin-bottom: 4px;
        }}

        .sidebar-chip-value {{
            font-size: 13px;
            font-weight: 600;
            color: #FFFFFF;
            word-break: break-all;
        }}

        /* ---------- Headings ---------- */
        h1 {{
            font-weight: 800 !important;
            letter-spacing: -0.8px;
            color: {TEXT} !important;
            padding-bottom: 4px;
        }}

        h2, h3 {{
            font-weight: 700 !important;
            letter-spacing: -0.3px;
            color: {TEXT} !important;
        }}

        .page-subtitle {{
            color: {TEXT_MUTED};
            font-size: 14px;
            margin-top: -8px;
            margin-bottom: 22px;
        }}

        /* ---------- Metric Cards ---------- */
        .metric-card {{
            background: {CARD_BG};
            border: 1px solid {BORDER};
            border-radius: 14px;
            padding: 20px 22px;
            min-height: 108px;
            box-shadow: 0 1px 2px rgba(15, 27, 45, 0.04);
            transition: box-shadow 0.2s ease, border-color 0.2s ease;
        }}

        .metric-card:hover {{
            box-shadow: 0 4px 14px rgba(15, 27, 45, 0.07);
            border-color: #D0D9E6;
        }}

        .metric-label {{
            color: {TEXT_MUTED};
            font-size: 11.5px;
            font-weight: 600;
            letter-spacing: 0.8px;
            text-transform: uppercase;
        }}

        .metric-value {{
            color: {TEXT};
            font-size: 26px;
            font-weight: 800;
            letter-spacing: -0.5px;
            margin-top: 10px;
            line-height: 1.15;
            word-break: break-word;
        }}

        .metric-value.success {{ color: {SUCCESS_TEXT}; }}
        .metric-value.danger  {{ color: {DANGER};  }}
        .metric-value.warn    {{ color: {WARN};    }}

        /* ---------- Section Headers ---------- */
        .section-title {{
            font-size: 15px;
            font-weight: 700;
            color: {TEXT};
            letter-spacing: -0.2px;
            margin: 26px 0 10px 0;
            padding-bottom: 8px;
            border-bottom: 1px solid {BORDER};
        }}

        /* ---------- Status Banner ---------- */
        .status-banner {{
            border-radius: 12px;
            padding: 14px 18px;
            font-size: 13.5px;
            font-weight: 500;
            line-height: 1.5;
            margin: 8px 0 4px 0;
            border-left: 4px solid;
        }}

        .status-banner.info {{
            background: {BLUE_LIGHT};
            border-color: {BLUE};
            color: #1E3A8A;
        }}

        .status-banner.warn {{
            background: {WARN_BG};
            border-color: {WARN};
            color: #7A4A00;
        }}

        .status-banner.success {{
            background: {SUCCESS_BG};
            border-color: {SUCCESS};
            color: #0B5A33;
        }}

        .status-banner.danger {{
            background: {DANGER_BG};
            border-color: {DANGER};
            color: #7A1C14;
        }}

        /* ---------- Workflow Steps ---------- */
        .step-card {{
            background: {CARD_BG};
            border: 1px solid {BORDER};
            border-radius: 10px;
            padding: 12px 16px;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .step-num {{
            font-size: 11px;
            font-weight: 700;
            color: {BLUE};
            background: {BLUE_LIGHT};
            border-radius: 6px;
            padding: 3px 8px;
            letter-spacing: 0.5px;
        }}

        .step-label {{
            font-size: 13px;
            font-weight: 600;
            color: {TEXT};
        }}

        /* ---------- Buttons ---------- */
        div.stButton > button[kind="primary"] {{
            background: {BLUE};
            border: 1px solid {BLUE};
            color: white;
            min-height: 46px;
            font-weight: 650;
            border-radius: 10px;
            letter-spacing: 0.2px;
            transition: background 0.15s ease;
        }}

        div.stButton > button[kind="primary"]:hover {{
            background: #1D4ED8;
            border-color: #1D4ED8;
        }}

        div.stButton > button {{
            border-radius: 10px;
            font-weight: 600;
            letter-spacing: 0.2px;
        }}

        /* ---------- Sticky Action Bar ---------- */
        .sticky-action {{
            position: sticky;
            bottom: 0;
            z-index: 10;
            background: rgba(246, 248, 252, 0.96);
            backdrop-filter: blur(6px);
            border-top: 1px solid {BORDER};
            padding: 14px 0 4px 0;
            margin-top: 24px;
        }}

        /* ---------- Form ---------- */
        [data-testid="stForm"] {{
            background: {CARD_BG};
            border: 1px solid {BORDER};
            border-radius: 14px;
            padding: 22px 24px;
        }}

        /* ---------- Dataframe ---------- */
        [data-testid="stDataFrame"] {{
            border: 1px solid {BORDER};
            border-radius: 12px;
            overflow: hidden;
        }}

        /* ---------- Expander ---------- */
        [data-testid="stExpander"] {{
            border: 1px solid {BORDER};
            border-radius: 12px;
            background: {CARD_BG};
        }}

        /* ---------- Divider ---------- */
        hr {{
            border-color: {BORDER};
        }}

        /* ---------- Profile Card ---------- */
        .profile-card {{
            background: {CARD_BG};
            border: 1px solid {BORDER};
            border-radius: 16px;
            padding: 28px 26px;
            box-shadow: 0 1px 2px rgba(15, 27, 45, 0.04);
        }}

        .profile-avatar {{
            width: 76px;
            height: 76px;
            border-radius: 50%;
            background: {BLUE_LIGHT};
            color: {BLUE};
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 26px;
            font-weight: 800;
            letter-spacing: 1px;
            margin: 0 auto 14px auto;
            border: 1px solid #D6E2FF;
        }}

        .profile-name {{
            text-align: center;
            font-size: 17px;
            font-weight: 700;
            color: {TEXT};
            letter-spacing: -0.2px;
            margin-bottom: 2px;
        }}

        .profile-role {{
            text-align: center;
            font-size: 11.5px;
            font-weight: 600;
            letter-spacing: 1.2px;
            text-transform: uppercase;
            color: {TEXT_MUTED};
        }}

        /* ---------- Info Grid ---------- */
        .info-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 18px 28px;
            margin-top: 4px;
        }}

        .info-row {{
            border-bottom: 1px dashed #EEF1F6;
            padding-bottom: 12px;
        }}

        .info-label {{
            font-size: 10.5px;
            font-weight: 700;
            letter-spacing: 1.2px;
            text-transform: uppercase;
            color: {TEXT_MUTED};
            margin-bottom: 4px;
        }}

        .info-value {{
            font-size: 14.5px;
            font-weight: 600;
            color: {TEXT};
            letter-spacing: -0.1px;
            word-break: break-all;
        }}

        .info-value.mono {{
            font-family: 'SF Mono', Menlo, Consolas, monospace;
            font-size: 13px;
            letter-spacing: 0;
        }}

        /* ---------- Recommendation Hero ---------- */
        .reco-hero {{
            display: flex;
            align-items: center;
            gap: 20px;
            border: 1px solid;
            border-left-width: 6px;
            border-radius: 14px;
            padding: 22px 26px;
            margin-bottom: 8px;
        }}

        .reco-icon {{
            font-size: 34px;
            line-height: 1;
        }}

        .reco-label {{
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 1.2px;
            text-transform: uppercase;
            margin-bottom: 4px;
        }}

        .reco-value {{
            font-size: 24px;
            font-weight: 800;
            color: {TEXT};
            letter-spacing: -0.4px;
        }}

        .compliance-badge {{
            display: inline-block;
            padding: 5px 10px;
            background: {WARN_BG};
            color: #7A4A00;
            border-radius: 6px;
            font-size: 11.5px;
            font-weight: 700;
            letter-spacing: 0.3px;
        }}

        /* ---------- Empty State ---------- */
        .empty-state {{
            background: {CARD_BG};
            border: 1px dashed #CBD5E1;
            border-radius: 14px;
            padding: 40px 24px;
            text-align: center;
            margin: 16px 0;
        }}

        .empty-icon {{
            font-size: 34px;
            margin-bottom: 10px;
        }}

        .empty-title {{
            font-size: 16px;
            font-weight: 700;
            color: {TEXT};
            margin-bottom: 6px;
        }}

        .empty-body {{
            font-size: 13.5px;
            color: {TEXT_MUTED};
            line-height: 1.6;
        }}

        /* ---------- Context Bar (customer context in pages) ---------- */
        .context-bar {{
            background: linear-gradient(135deg, #EFF4FF 0%, #E0EAFF 100%);
            border: 1px solid #C7D8FF;
            border-radius: 14px;
            padding: 16px 20px;
            margin-bottom: 18px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
        }}

        .context-bar-label {{
            font-size: 10.5px;
            font-weight: 700;
            letter-spacing: 1.3px;
            text-transform: uppercase;
            color: {BLUE};
            margin-bottom: 4px;
        }}

        .context-bar-value {{
            font-size: 15px;
            font-weight: 700;
            color: {TEXT};
        }}

        .context-bar-sub {{
            font-size: 12px;
            color: {TEXT_MUTED};
            margin-top: 2px;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================
# 4. REUSABLE COMPONENTS
# ==========================================

def metric_card(label: str, value: str, variant: str = ""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value {variant}">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_title(text: str):
    st.markdown(
        f'<div class="section-title">{text}</div>',
        unsafe_allow_html=True,
    )


def status_banner(text: str, kind: str = "info"):
    icon = {"info": "ℹ", "warn": "⚠", "success": "✓", "danger": "✕"}.get(kind, "")
    st.markdown(
        f'<div class="status-banner {kind}">{icon} {text}</div>',
        unsafe_allow_html=True,
    )


def page_header(title: str, subtitle: str):
    st.title(title)
    st.markdown(
        f'<div class="page-subtitle">{subtitle}</div>',
        unsafe_allow_html=True,
    )


def workflow_step(number: int, label: str):
    st.markdown(
        f"""
        <div class="step-card">
            <span class="step-num">{number:02d}</span>
            <span class="step-label">{label}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def empty_state(icon: str, title: str, body: str):
    st.markdown(
        f"""
        <div class="empty-state">
            <div class="empty-icon">{icon}</div>
            <div class="empty-title">{title}</div>
            <div class="empty-body">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def info_row(label: str, value: str, mono: bool = False):
    cls = "info-value mono" if mono else "info-value"
    st.markdown(
        f"""
        <div class="info-row">
            <div class="info-label">{label}</div>
            <div class="{cls}">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def customer_context_bar():
    """Compact context strip showing the currently selected customer."""
    customer = st.session_state.get("credigo_customer")
    customer_id = st.session_state.get("credigo_selected_customer_id")
    application_id = st.session_state.get("credigo_selected_application_id")

    if not customer_id:
        return

    name = "Selected Customer"
    if customer:
        fn = str(customer.get("first_name", "")).strip()
        ln = str(customer.get("last_name", "")).strip()
        name = f"{fn} {ln}".strip() or name

    st.markdown(
        f"""
        <div class="context-bar">
            <div>
                <div class="context-bar-label">Active Customer</div>
                <div class="context-bar-value">{name}</div>
                <div class="context-bar-sub">
                    ID: <span style="font-family:'SF Mono',Menlo,monospace;">{customer_id}</span>
                </div>
            </div>
            <div style="text-align:right;">
                <div class="context-bar-label">Loan Application</div>
                <div class="context-bar-value" style="font-family:'SF Mono',Menlo,monospace;font-size:13px;">
                    {application_id if application_id else "— not selected —"}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


ERROR_MESSAGES = {
    400: "The request was malformed. Please check your inputs.",
    401: "Your session has expired. Please sign in again.",
    403: "You don't have permission to perform this action.",
    404: "The requested record was not found.",
    409: "This record already exists.",
    422: "Some fields are invalid. Please review and resubmit.",
    500: "The server encountered an error. Please contact support with the details below.",
}


def show_api_error(exc, context: str):
    status = getattr(exc, "status", None)
    msg = ERROR_MESSAGES.get(status, "An unexpected error occurred.")
    st.error(f"**{context}** — {msg}")
    with st.expander("Technical details (for support)"):
        st.code(f"status={status}\n{exc}")


# ==========================================
# 5. DISPLAY INVESTIGATION REPORT
# ==========================================

def show_report(result: dict):

    report = result.get("credit_risk_report") or {}
    prediction = result.get("ml_prediction") or {}
    policy = result.get("policy_assessment") or {}
    summary = policy.get("policy_summary") or {}

    section_title("Investigation Result")
    st.caption(f"Status: {result.get('status', 'Unknown')}")

    recommendation = (
        report.get("recommendation")
        or result.get("ai_recommend")
        or "Not available"
    )

    reco_map = {
        "recommend_approval": (SUCCESS, SUCCESS_BG, "Recommended for Approval", "✓"),
        "recommend_rejection": (DANGER, DANGER_BG, "Recommended for Rejection", "✕"),
        "manual_review_required": (WARN, WARN_BG, "Manual Review Required", "⚠"),
    }
    color, bg, label, icon = reco_map.get(
        recommendation,
        (TEXT_MUTED, "#F1F5F9", str(recommendation).replace("_", " ").title(), "–"),
    )

    st.markdown(
        f"""
        <div class="reco-hero" style="border-color:{color};background:{bg};">
            <div class="reco-icon" style="color:{color};">{icon}</div>
            <div>
                <div class="reco-label" style="color:{color};">AI Recommendation</div>
                <div class="reco-value">{label}</div>
            </div>
            <div style="margin-left:auto;">
                <span class="compliance-badge">⚠ Decision support only · Human approval required</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        probability = prediction.get("default_probability")
        value = (
            f"{float(probability):.2%}"
            if isinstance(probability, (int, float))
            else "Not available"
        )
        p_variant = ""
        if isinstance(probability, (int, float)):
            if probability >= 0.5:
                p_variant = "danger"
            elif probability >= 0.25:
                p_variant = "warn"
            else:
                p_variant = "success"
        metric_card("Default Probability", value, p_variant)

    with col2:
        score = prediction.get("risk_score")
        metric_card(
            "Risk Score",
            str(score) if score is not None else "Not available",
        )

    if recommendation == "manual_review_required":
        status_banner(
            "Manual review is required. This is decision support, "
            "not a final lending decision.",
            "warn",
        )
    elif recommendation in ("recommend_approval", "recommend_rejection"):
        status_banner(
            "This is an AI recommendation only. An authorized human "
            "officer makes the final decision.",
            "info",
        )

    section_title("Executive Summary")
    st.write(
        report.get(
            "executive_summary",
            "No report summary was returned.",
        )
    )

    left, right = st.columns(2)

    with left:
        section_title("Key Risk Factors")
        factors = report.get("key_risk_factors") or []
        if factors:
            for item in factors:
                with st.expander(item.get("factor", "Risk Factor")):
                    st.write(
                        item.get("explanation", "No explanation provided.")
                    )
                    st.caption(
                        f"Severity: {item.get('severity', 'UNKNOWN')}"
                    )
                    for evidence in item.get("evidence", []):
                        st.caption(
                            f"{evidence.get('policy_id', '')} / "
                            f"{evidence.get('check_id', '')} — "
                            f"{evidence.get('status', '')}"
                        )
        else:
            st.caption("No risk factors returned.")

    with right:
        section_title("Missing Information")
        missing = report.get("missing_information") or []
        if missing:
            for item in missing:
                st.write(f"• {item}")
        else:
            st.caption("No missing information returned.")

        section_title("Verified Findings")
        findings = report.get("verified_findings") or []
        if findings:
            for item in findings:
                st.write(f"• {item}")
        else:
            st.caption("No verified findings returned.")

    limitations = report.get("limitations") or []
    if limitations:
        with st.expander("Report Limitations"):
            for item in limitations:
                st.write(f"• {item}")

    section_title("Policy Assessment")

    p1, p2, p3, p4 = st.columns(4)
    with p1:
        metric_card("Passed", str(summary.get("passed", 0)), "success")
    with p2:
        metric_card("Failed", str(summary.get("failed", 0)), "danger")
    with p3:
        metric_card("Unverified", str(summary.get("unverified", 0)), "warn")
    with p4:
        metric_card("Not Required", str(summary.get("not_required", 0)))

    records = policy.get("evidence_records") or []
    if records:
        rows = []
        for item in records:
            rows.append({
                "Policy ID": item.get("policy_id", ""),
                "Check": item.get("check_id", ""),
                "Status": item.get("status", ""),
                "Reason": item.get("reason", ""),
                "Observed": item.get("observed_value"),
                "Expected": item.get("expected_value"),
                "Source": item.get("source", ""),
            })
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        status_banner(
            "The API response did not include policy evidence records.",
            "info",
        )

    # Officer decision
    section_title("Officer Decision")
    with st.form("decision_form"):
        st.caption(
            "Record your final decision. AI output is advisory only — "
            "the decision is yours."
        )
        decision = st.radio(
            "Decision",
            ["Approve", "Reject", "Request more information"],
            horizontal=True,
        )
        rationale = st.text_area(
            "Rationale (required)",
            placeholder="Explain your reasoning for this decision…",
        )
        confirmed = st.checkbox("I confirm this is my authorized decision.")
        submitted_decision = st.form_submit_button(
            "Record Decision",
            type="primary",
            use_container_width=True,
        )

    if submitted_decision:
        if not rationale.strip() or not confirmed:
            st.error("Rationale and confirmation are required.")
        else:
            st.session_state["credigo_last_decision"] = {
                "decision": decision,
                "rationale": rationale.strip(),
                "recommendation": recommendation,
            }
            st.success("Decision recorded.")

    with st.expander("Raw API Response"):
        st.json(result)


# ==========================================
# 6. CUSTOMER 360° + RECORD MANAGEMENT
# ==========================================

def show_customer_360(profile: dict):

    customer_id = str(profile.get("customer_id"))

    if customer_id and customer_id != "None":
        try:
            profile = get_customer_profile(customer_id)
        except ApiError as exc:
            show_api_error(exc, "Unable to refresh customer profile")

    success_message = st.session_state.pop("credigo_application_success", None)
    if success_message:
        st.success(success_message)

    section_title("Customer 360° Overview")

    accounts = profile.get("accounts") or []
    employment = profile.get("employment_records") or []
    credit_histories = profile.get("credit_histories") or []
    loans = profile.get("loans") or []
    applications = profile.get("loan_applications") or []
    repayments = profile.get("repayment_records") or []

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Bank Accounts", str(len(accounts)))
    with col2:
        metric_card("Employment", str(len(employment)))
    with col3:
        metric_card("Loans", str(len(loans)))
    with col4:
        metric_card("Applications", str(len(applications)))

    section_title("Manage Customer Records")
    st.caption("Select a category to add a new customer record.")

    buttons = [
        ("+ Add Employment", "employment"),
        ("+ Add Bank Account", "account"),
        ("+ Add Credit History", "credit"),
        ("+ Add Loan", "loan"),
        ("+ Add Repayment", "repayment"),
        ("+ Add Loan Application", "application"),
    ]

    for row_start in (0, 3):
        cols = st.columns(3)
        for col, (label, record_type) in zip(cols, buttons[row_start:row_start + 3]):
            with col:
                if st.button(
                    label,
                    key=f"add_{record_type}_btn",
                    use_container_width=True,
                ):
                    st.session_state["credigo_add_record_type"] = record_type
                    st.rerun()

    selected_record = st.session_state.get("credigo_add_record_type")

    # ======================================
    # EMPLOYMENT FORM
    # ======================================

    if selected_record == "employment":
        section_title("Add Employment Record")

        with st.form("add_employment_form"):
            company_name = st.text_input("Company Name *")
            job_title = st.text_input("Job Title *")
            employment_type = st.selectbox(
                "Employment Type",
                ["Full-time", "Part-time", "Self-employed", "Contract"],
            )
            monthly_income = st.number_input(
                "Monthly Income (THB) *", min_value=0.0, step=1000.0,
            )
            employment_start_date = st.date_input(
                "Employment Start Date", value=date.today(), max_value=date.today(),
            )

            c1, c2 = st.columns(2)
            save = c1.form_submit_button(
                "Save Employment Record", type="primary", use_container_width=True,
            )
            cancel = c2.form_submit_button("Cancel", use_container_width=True)

        if cancel:
            st.session_state.pop("credigo_add_record_type", None)
            st.rerun()

        if save:
            if not company_name.strip() or not job_title.strip():
                st.error("Company Name and Job Title are required.")
            elif monthly_income <= 0:
                st.error("Monthly Income must be greater than 0.")
            else:
                data = {
                    "company_name": company_name.strip(),
                    "job_title": job_title.strip(),
                    "employment_type": employment_type,
                    "monthly_income": monthly_income,
                    "employment_start_date": employment_start_date.isoformat(),
                }
                try:
                    with st.spinner("Saving employment record..."):
                        create_employment(customer_id, data)
                    st.success("Employment record saved successfully!")
                    st.session_state.pop("credigo_add_record_type", None)
                    st.rerun()
                except ApiError as exc:
                    show_api_error(exc, "Failed to save employment")

    # ======================================
    # BANK ACCOUNT FORM
    # ======================================

    elif selected_record == "account":
        section_title("Add Bank Account")

        with st.form("add_account_form"):
            account_number = st.text_input("Account Number *")
            bank_name = st.text_input("Bank Name *")
            account_type = st.selectbox(
                "Account Type", ["Savings", "Current", "Fixed Deposit", "Other"],
            )
            balance = st.number_input("Balance (THB)", min_value=0.0, step=1000.0)
            account_status = st.selectbox(
                "Account Status", ["Active", "Inactive", "Closed"],
            )
            opened_at = st.date_input(
                "Account Opening Date", value=date.today(), max_value=date.today(),
            )

            c1, c2 = st.columns(2)
            save = c1.form_submit_button(
                "Save Bank Account", type="primary", use_container_width=True,
            )
            cancel = c2.form_submit_button("Cancel", use_container_width=True)

        if cancel:
            st.session_state.pop("credigo_add_record_type", None)
            st.rerun()

        if save:
            if not account_number.strip() or not bank_name.strip():
                st.error("Account Number and Bank Name are required.")
            else:
                data = {
                    "account_number": account_number.strip(),
                    "bank_name": bank_name.strip(),
                    "account_type": account_type,
                    "balance": balance,
                    "account_status": account_status,
                    "opened_at": opened_at.isoformat(),
                }
                try:
                    with st.spinner("Saving bank account..."):
                        create_account(customer_id, data)
                    st.success("Bank account saved successfully!")
                    st.session_state.pop("credigo_add_record_type", None)
                    st.rerun()
                except ApiError as exc:
                    show_api_error(exc, "Failed to save bank account")

    # ======================================
    # CREDIT HISTORY FORM
    # ======================================

    elif selected_record == "credit":
        section_title("Add Credit History")

        with st.form("add_credit_form"):
            credit_score = st.number_input(
                "Credit Score *", min_value=300, max_value=850, value=650, step=1,
            )
            total_debt = st.number_input("Total Debt (THB)", min_value=0.0, step=1000.0)
            credit_utilization = st.number_input(
                "Credit Utilization (%)", min_value=0.0, max_value=100.0, step=1.0,
            )
            recorded_at = st.date_input(
                "Recorded Date", value=date.today(), max_value=date.today(),
            )

            c1, c2 = st.columns(2)
            save = c1.form_submit_button(
                "Save Credit History", type="primary", use_container_width=True,
            )
            cancel = c2.form_submit_button("Cancel", use_container_width=True)

        if cancel:
            st.session_state.pop("credigo_add_record_type", None)
            st.rerun()

        if save:
            data = {
                "credit_score": credit_score,
                "total_debt": total_debt,
                "credit_utilization": credit_utilization,
                "recorded_at": recorded_at.isoformat(),
            }
            try:
                with st.spinner("Saving credit history..."):
                    create_credit_history(customer_id, data)
                st.success("Credit history saved successfully!")
                st.session_state.pop("credigo_add_record_type", None)
                st.rerun()
            except ApiError as exc:
                show_api_error(exc, "Failed to save credit history")

    # ======================================
    # LOAN FORM
    # ======================================

    elif selected_record == "loan":
        section_title("Add Loan Record")

        with st.form("add_loan_form"):
            loan_amount = st.number_input(
                "Loan Amount (THB) *", min_value=1.0, step=10000.0,
            )
            interest_rate = st.number_input(
                "Interest Rate (%) *", min_value=0.0, max_value=100.0, step=0.1,
            )
            loan_term = st.number_input(
                "Loan Term (Months) *", min_value=1, max_value=600, value=12, step=1,
            )
            loan_status = st.selectbox(
                "Loan Status",
                ["Pending", "Active", "Completed", "Defaulted", "Rejected"],
            )
            application_date = st.date_input(
                "Application Date", value=date.today(), max_value=date.today(),
            )

            c1, c2 = st.columns(2)
            save = c1.form_submit_button(
                "Save Loan", type="primary", use_container_width=True,
            )
            cancel = c2.form_submit_button("Cancel", use_container_width=True)

        if cancel:
            st.session_state.pop("credigo_add_record_type", None)
            st.rerun()

        if save:
            data = {
                "loan_amount": loan_amount,
                "interest_rate": interest_rate,
                "loan_term": loan_term,
                "loan_status": loan_status,
                "application_date": application_date.isoformat(),
            }
            try:
                with st.spinner("Saving loan..."):
                    create_loan(customer_id, data)
                st.success("Loan record saved successfully!")
                st.session_state.pop("credigo_add_record_type", None)
                st.rerun()
            except ApiError as exc:
                show_api_error(exc, "Failed to save loan")

    # ======================================
    # REPAYMENT FORM
    # ======================================

    elif selected_record == "repayment":
        section_title("Add Repayment Record")

        if not loans:
            st.warning(
                "This customer has no loan records. "
                "Please add a Loan before adding a Repayment."
            )
            if st.button("Back", use_container_width=True):
                st.session_state.pop("credigo_add_record_type", None)
                st.rerun()
        else:
            loan_options = {
                int(item["loan_id"]): item
                for item in loans
                if item.get("loan_id") is not None
            }

            if not loan_options:
                st.warning("No valid Loan ID was found in this profile.")
                if st.button("Back", use_container_width=True):
                    st.session_state.pop("credigo_add_record_type", None)
                    st.rerun()
            else:
                with st.form("add_repayment_form"):
                    loan_id = st.selectbox(
                        "Select Loan *",
                        options=list(loan_options.keys()),
                        format_func=lambda value: (
                            f"Loan #{value} — "
                            f"{loan_options[value].get('loan_amount', 'N/A')} THB"
                        ),
                    )
                    payment_amount = st.number_input(
                        "Payment Amount (THB) *", min_value=0.01, step=1000.0,
                    )
                    due_date = st.date_input("Due Date", value=date.today())
                    payment_date = st.date_input("Payment Date", value=date.today())
                    payment_status = st.selectbox(
                        "Payment Status", ["Paid", "Pending", "Overdue", "Partial"],
                    )
                    has_payment_date = st.checkbox(
                        "Payment has been made", value=True,
                    )

                    c1, c2 = st.columns(2)
                    save = c1.form_submit_button(
                        "Save Repayment", type="primary", use_container_width=True,
                    )
                    cancel = c2.form_submit_button("Cancel", use_container_width=True)

                if cancel:
                    st.session_state.pop("credigo_add_record_type", None)
                    st.rerun()

                if save:
                    data = {
                        "loan_id": loan_id,
                        "payment_amount": payment_amount,
                        "due_date": due_date.isoformat(),
                        "payment_date": (
                            payment_date.isoformat() if has_payment_date else None
                        ),
                        "payment_status": payment_status,
                    }
                    try:
                        with st.spinner("Saving repayment..."):
                            create_repayment(customer_id, data)
                        st.success("Repayment saved successfully!")
                        st.session_state.pop("credigo_add_record_type", None)
                        st.rerun()
                    except ApiError as exc:
                        show_api_error(exc, "Failed to save repayment")

    # ======================================
    # LOAN APPLICATION
    # ======================================

    elif selected_record == "application":
        section_title("Loan Application")

        success_message = st.session_state.pop(
            "credigo_application_success", None
        )
        if success_message:
            st.success(success_message)

        if applications:
            application_mode = st.radio(
                "Choose an action",
                ["Select Existing Application", "Create New Application"],
                horizontal=True,
                key="credigo_application_mode",
            )
        else:
            st.info(
                "This customer has no existing loan applications. "
                "Create a new application to continue."
            )
            application_mode = "Create New Application"

        # ---------- OPTION 1: SELECT EXISTING ----------
        if application_mode == "Select Existing Application":
            st.markdown("#### Existing Loan Applications")

            valid_applications = {
                str(item["application_id"]): item
                for item in applications
                if item.get("application_id") is not None
            }

            if not valid_applications:
                st.warning("No valid Application ID was found in this profile.")
            else:
                selected_application_id = st.selectbox(
                    "Select Loan Application *",
                    options=list(valid_applications.keys()),
                    format_func=lambda app_id: (
                        f"{app_id[:8]}... | "
                        f"{valid_applications[app_id].get('application_status', 'Unknown')} | "
                        f"{valid_applications[app_id].get('requested_amount', 'N/A')} THB"
                    ),
                    key="credigo_existing_application_selector",
                )

                selected_application = valid_applications[selected_application_id]

                col1, col2, col3 = st.columns(3)
                with col1:
                    metric_card(
                        "Requested Amount",
                        f"{selected_application.get('requested_amount', 'N/A')} THB",
                    )
                with col2:
                    metric_card(
                        "Requested Term",
                        f"{selected_application.get('requested_term_months', 'N/A')} Months",
                    )
                with col3:
                    metric_card(
                        "Application Status",
                        str(selected_application.get("application_status", "Unknown")),
                    )

                st.caption(f"Application ID: {selected_application_id}")

                b1, b2 = st.columns(2)
                with b1:
                    if st.button(
                        "Use This Application",
                        type="primary",
                        use_container_width=True,
                        key="use_existing_application",
                    ):
                        st.session_state["credigo_selected_application_id"] = selected_application_id
                        st.session_state["credigo_selected_customer_id"] = customer_id
                        st.success("Existing Loan Application selected successfully.")
                with b2:
                    if st.button(
                        "Cancel",
                        use_container_width=True,
                        key="cancel_existing_application",
                    ):
                        st.session_state.pop("credigo_add_record_type", None)
                        st.rerun()

        # ---------- OPTION 2: CREATE NEW ----------
        elif application_mode == "Create New Application":
            st.markdown("#### Create New Loan Application")

            with st.form("add_application_form"):
                requested_amount = st.number_input(
                    "Requested Amount (THB) *", min_value=1.0, step=10000.0, value=100000.0,
                )
                requested_term_months = st.number_input(
                    "Requested Term (Months) *", min_value=1, max_value=600, value=12, step=1,
                )
                application_status = st.selectbox(
                    "Application Status", ["Submitted", "Under Review"],
                )

                c1, c2 = st.columns(2)
                save = c1.form_submit_button(
                    "Create Loan Application", type="primary", use_container_width=True,
                )
                cancel = c2.form_submit_button("Cancel", use_container_width=True)

            if cancel:
                st.session_state.pop("credigo_add_record_type", None)
                st.rerun()

            if save:
                if requested_amount <= 0:
                    st.error("Requested Amount must be greater than 0.")
                elif requested_term_months <= 0:
                    st.error("Requested Term must be greater than 0.")
                else:
                    data = {
                        "requested_amount": requested_amount,
                        "requested_term_months": int(requested_term_months),
                        "application_status": application_status,
                    }
                    try:
                        with st.spinner("Creating Loan Application..."):
                            result = create_loan_application(customer_id, data)

                        new_application_id = (
                            result.get("application_id")
                            if isinstance(result, dict)
                            else None
                        )

                        if new_application_id:
                            st.session_state["credigo_selected_application_id"] = str(new_application_id)
                            st.session_state["credigo_selected_customer_id"] = customer_id
                            st.session_state["credigo_application_success"] = (
                                "Loan Application created successfully. "
                                f"Application ID: {new_application_id}"
                            )
                        else:
                            st.session_state["credigo_application_success"] = (
                                "Loan Application created successfully. "
                                "Please refresh the profile to retrieve its ID."
                            )

                        st.session_state.pop("credigo_add_record_type", None)
                        st.rerun()

                    except ApiError as exc:
                        show_api_error(exc, "Failed to create Loan Application")

    # ======================================
    # DISPLAY CUSTOMER RECORDS
    # ======================================

    records_to_display = [
        ("Employment Records", employment),
        ("Bank Accounts", accounts),
        ("Credit History", credit_histories),
        ("Loan Records", loans),
        ("Repayment Records", repayments),
        ("Loan Applications", applications),
    ]

    for title, records in records_to_display:
        with st.expander(title, expanded=(title == "Employment Records")):
            if records:
                st.dataframe(
                    pd.DataFrame(records),
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.info(f"No {title.lower()} found.")


# ==========================================
# 7. SIDEBAR NAVIGATION (no Test Backend button)
# ==========================================

with st.sidebar:
    st.markdown('<div class="brand">CREDIGO</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="brand-sub">Credit Risk Intelligence</div>',
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown(
        '<div class="sidebar-label">Workspace</div>',
        unsafe_allow_html=True,
    )

    page = st.radio(
        "WORKSPACE",
        ["Dashboard", "Customer Search", "Credit Investigation"],
        label_visibility="collapsed",
        key="credigo_page",
    )

    st.divider()

    active_customer_id = st.session_state.get("credigo_selected_customer_id")
    active_customer = st.session_state.get("credigo_customer")
    if active_customer_id:
        name = ""
        if active_customer:
            fn = str(active_customer.get("first_name", "")).strip()
            ln = str(active_customer.get("last_name", "")).strip()
            name = f"{fn} {ln}".strip()
        st.markdown(
            f"""
            <div class="sidebar-chip">
                <div class="sidebar-chip-label">Active Customer</div>
                <div class="sidebar-chip-value">{name or 'Selected'}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    active_application_id = st.session_state.get("credigo_selected_application_id")
    if active_application_id:
        st.markdown(
            f"""
            <div class="sidebar-chip">
                <div class="sidebar-chip-label">Loan Application</div>
                <div class="sidebar-chip-value" style="font-family:'SF Mono',Menlo,monospace;font-size:11px;">
                    {str(active_application_id)[:18]}...
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="sidebar-meta">Internal Banking Decision Support<br>'
        'Credigo MVP v1.0</div>',
        unsafe_allow_html=True,
    )


# ==========================================
# 8. DASHBOARD PAGE
# ==========================================

if page == "Dashboard":

    page_header(
        "Credit Risk Dashboard",
        "System overview and investigation workspace.",
    )

    try:
        health = check_health()
        api_ok = health.get("status") == "healthy"
        health_error = None
    except ApiError as exc:
        api_ok = False
        health_error = str(exc)

    col1, col2, col3 = st.columns(3)

    with col1:
        metric_card(
            "Backend API",
            "Online" if api_ok else "Offline",
            "success" if api_ok else "danger",
        )

    with col2:
        has_customer = bool(st.session_state.get("credigo_selected_customer_id"))
        metric_card(
            "Active Customer",
            "Selected" if has_customer else "None",
            "success" if has_customer else "",
        )

    with col3:
        has_result = bool(st.session_state.get("credigo_last_result"))
        metric_card(
            "Last Investigation",
            "Ready" if has_result else "No result",
            "success" if has_result else "",
        )

    st.write("")

    if api_ok:
        status_banner("FastAPI health check succeeded.", "success")
    else:
        status_banner(
            "Cannot connect to the backend health endpoint.",
            "danger",
        )
        if health_error:
            st.code(health_error)

    if st.session_state.get("credigo_selected_customer_id"):
        customer_context_bar()

        c1, c2 = st.columns(2)
        with c1:
            if st.button(
                "Open Customer Search →",
                use_container_width=True,
                key="dash_go_search",
            ):
                st.session_state["credigo_page"] = "Customer Search"
                st.rerun()
        with c2:
            if st.button(
                "Start Credit Investigation →",
                type="primary",
                use_container_width=True,
                key="dash_go_investigation",
            ):
                st.session_state["credigo_page"] = "Credit Investigation"
                st.rerun()

    section_title("Investigation Workflow")

    steps = [
        "Customer Retrieval",
        "Data Validation",
        "ML Risk Prediction",
        "Credit Policy Retrieval",
        "AI Analysis",
        "Policy Assessment",
        "Evidence Aggregation",
        "Risk Report Generation",
        "Report Validation",
    ]

    cols = st.columns(3)
    for i, step in enumerate(steps):
        with cols[i % 3]:
            workflow_step(i + 1, step)

    st.write("")
    status_banner(
        "Use Customer Search to find a customer, then proceed to "
        "Credit Investigation.",
        "info",
    )


# ==========================================
# 9. CUSTOMER SEARCH PAGE
# ==========================================

elif page == "Customer Search":

    page_header(
        "Customer Search",
        "Search and retrieve customer information using National ID.",
    )

    status_banner(
        "Search for an existing customer using their 13-digit "
        "National ID.",
        "info",
    )

    col_search, col_register = st.columns([2, 1])

    with col_search:
        with st.form("customer_search_form"):
            national_id_input = st.text_input(
                "National ID",
                max_chars=13,
                placeholder="Enter 13-digit National ID",
            ).strip()

            search_submitted = st.form_submit_button(
                "Search Customer",
                type="primary",
                use_container_width=True,
            )

    with col_register:
        st.write("")
        st.write("")
        if st.button("+ Register New Customer", use_container_width=True):
            st.session_state["credigo_show_register_form"] = not st.session_state.get(
                "credigo_show_register_form", False
            )
            st.rerun()

    if st.session_state.get("credigo_show_register_form", False):
        section_title("Register New Customer")

        with st.form("customer_register_form"):
            st.caption("Enter the customer's personal information.")

            national_id = st.text_input(
                "National ID *",
                max_chars=13,
                placeholder="13 digits",
            )

            col1, col2 = st.columns(2)

            with col1:
                first_name = st.text_input("First Name *")
                date_of_birth = st.date_input(
                    "Date of Birth *",
                    value=date(2000, 1, 1),
                    max_value=date.today(),
                )
                gender = st.selectbox(
                    "Gender", ["", "Male", "Female", "Other"]
                )
                phone_number = st.text_input("Phone Number")

            with col2:
                last_name = st.text_input("Last Name *")
                email = st.text_input("Email")
                marital_status = st.selectbox(
                    "Marital Status",
                    ["", "Single", "Married", "Divorced", "Widowed"],
                )
                education = st.text_input("Education")

            address = st.text_area("Address")

            register_submitted = st.form_submit_button(
                "Register Customer",
                type="primary",
                use_container_width=True,
            )

        if register_submitted:
            if len(national_id) != 13 or not national_id.isdigit():
                st.error("National ID must contain exactly 13 digits.")
            elif not first_name.strip() or not last_name.strip():
                st.error("First Name and Last Name are required.")
            else:
                customer_data = {
                    "national_id": national_id,
                    "first_name": first_name.strip(),
                    "last_name": last_name.strip(),
                    "date_of_birth": date_of_birth.isoformat(),
                    "gender": gender or None,
                    "email": email.strip() or None,
                    "phone_number": phone_number.strip() or None,
                    "address": address.strip() or None,
                    "marital_status": marital_status or None,
                    "education": education.strip() or None,
                }

                try:
                    with st.spinner("Registering customer..."):
                        new_customer = register_customer(customer_data)

                    st.session_state["credigo_customer"] = new_customer
                    st.session_state["credigo_selected_customer_id"] = str(
                        new_customer["customer_id"]
                    )
                    st.session_state["credigo_show_register_form"] = False
                    st.session_state.pop("credigo_customer_error", None)
                    st.session_state.pop("credigo_customer_not_found", None)
                    st.success("Customer registered successfully!")
                    st.rerun()

                except ApiError as exc:
                    if getattr(exc, "status", None) == 409:
                        st.error("This National ID is already registered.")
                    else:
                        show_api_error(exc, "Registration failed")
                except Exception as exc:
                    st.error(f"Registration failed: {exc}")

    if search_submitted:
        st.session_state.pop("credigo_customer", None)
        st.session_state.pop("credigo_customer_profile", None)
        st.session_state.pop("credigo_customer_error", None)
        st.session_state.pop("credigo_customer_not_found", None)

        if len(national_id_input) != 13 or not national_id_input.isdigit():
            st.session_state["credigo_customer_error"] = (
                "National ID must contain exactly 13 digits."
            )
        else:
            try:
                with st.spinner("Loading Customer 360° Profile..."):
                    customer = search_customer(national_id_input)
                    customer_id = str(customer["customer_id"])
                    profile = get_customer_profile(customer_id)

                st.session_state["credigo_customer"] = customer
                st.session_state["credigo_customer_profile"] = profile

            except ApiError as exc:
                if getattr(exc, "status", None) == 404:
                    st.session_state["credigo_customer_not_found"] = True
                else:
                    st.session_state["credigo_customer_error"] = str(exc)
            except Exception as exc:
                st.session_state["credigo_customer_error"] = str(exc)

    if st.session_state.get("credigo_customer_error"):
        st.error(st.session_state["credigo_customer_error"])

    if st.session_state.get("credigo_customer_not_found"):
        empty_state(
            "🔍",
            "No customer found",
            f"No record matches National ID <b>{national_id_input}</b>. "
            "Double-check the number, or register the customer.",
        )

    customer = st.session_state.get("credigo_customer")

    if customer:

        st.write("")
        status_banner("Customer successfully retrieved.", "success")
        section_title("Customer Profile")

        customer_id = str(customer.get("customer_id", "N/A"))
        first_name = str(customer.get("first_name", "N/A"))
        last_name = str(customer.get("last_name", "N/A"))
        date_of_birth = str(customer.get("date_of_birth", "N/A"))

        initials = (
            (first_name[:1] + last_name[:1]).upper()
            if first_name != "N/A" or last_name != "N/A"
            else "CU"
        )
        full_name = (
            f"{first_name} {last_name}"
            if first_name != "N/A" or last_name != "N/A"
            else "Customer"
        )

        col1, col2 = st.columns([1, 2.4], gap="medium")

        with col1:
            st.markdown(
                f"""
                <div class="profile-card">
                    <div class="profile-avatar">{initials}</div>
                    <div class="profile-name">{full_name}</div>
                    <div class="profile-role">Customer Record</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown('<div class="profile-card">', unsafe_allow_html=True)
            st.markdown('<div class="info-grid">', unsafe_allow_html=True)
            info_row("Customer ID", customer_id, mono=True)
            info_row("First Name", first_name)
            info_row("Last Name", last_name)
            info_row("Date of Birth", date_of_birth)
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        customer_profile = st.session_state.get("credigo_customer_profile")
        if customer_profile:
            show_customer_360(customer_profile)

        st.session_state["credigo_selected_customer_id"] = customer_id

        section_title("Next Step")
        st.write(
            "The customer record has been retrieved. You may proceed "
            "to Credit Investigation to run the full risk assessment."
        )

        st.markdown('<div class="sticky-action">', unsafe_allow_html=True)
        if st.button(
            "Continue to Credit Investigation →",
            type="primary",
            use_container_width=True,
        ):
            st.session_state["credigo_go_to_investigation"] = True
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# 10. CREDIT INVESTIGATION PAGE
# ==========================================

elif page == "Credit Investigation":

    page_header(
        "Credit Investigation",
        "Run the existing LangGraph investigation through FastAPI.",
    )

    status_banner(
        "AI output is decision support only. It does not approve or "
        "reject a loan. An authorized human officer must make the "
        "final decision.",
        "warn",
    )

    st.write("")

    customer_context_bar()

    selected_customer_id = st.session_state.get(
        "credigo_selected_customer_id", ""
    )

    with st.form("investigation_form"):
        customer_id = st.text_input(
            "Customer ID (UUID)",
            value=selected_customer_id,
            placeholder="Enter customer UUID",
        ).strip()

        application_id = st.text_input(
            "Loan Application ID (UUID)",
            value=st.session_state.get("credigo_selected_application_id", ""),
            placeholder="Select or create a Loan Application first",
        ).strip()

        submitted = st.form_submit_button(
            "Start Investigation",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        if not customer_id or not application_id:
            st.error("Please enter both Customer ID and Application ID.")
        else:
            try:
                with st.spinner(
                    "Investigation is running. This may take a few minutes..."
                ):
                    result = run_investigation(customer_id, application_id)

                st.session_state["credigo_last_result"] = result
                st.session_state.pop("credigo_last_error", None)
                st.success("Investigation request completed.")

            except ApiError as exc:
                st.session_state.pop("credigo_last_result", None)
                st.session_state["credigo_last_error"] = str(exc)
            except Exception as exc:
                st.session_state.pop("credigo_last_result", None)
                st.session_state["credigo_last_error"] = (
                    f"Unexpected frontend error: {exc}"
                )

    if st.session_state.get("credigo_last_error"):
        st.error(st.session_state["credigo_last_error"])

    result = st.session_state.get("credigo_last_result")
    if result:
        show_report(result)


# ==========================================
# 11. NAVIGATION FROM CUSTOMER SEARCH
# ==========================================

if st.session_state.pop("credigo_go_to_investigation", False):
    st.session_state["credigo_last_result"] = None
    st.session_state.pop("credigo_last_error", None)
    st.session_state["credigo_page"] = "Credit Investigation"
    st.rerun()