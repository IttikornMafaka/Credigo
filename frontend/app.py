import streamlit as st
import pandas as pd

from api.client import (
    check_health,
    run_investigation,
    ApiError,
    search_customer,
    get_customer,
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
SUCCESS = "#0F9D58"
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
            color: #7B8DA6;
            margin-bottom: 4px;
        }}

        .sidebar-meta {{
            font-size: 11px;
            color: #7B8DA6;
            letter-spacing: 0.5px;
            line-height: 1.6;
        }}

        .sidebar-label {{
            font-size: 10.5px;
            font-weight: 700;
            letter-spacing: 1.8px;
            text-transform: uppercase;
            color: #7B8DA6;
            margin-bottom: 8px;
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

        .metric-value.success {{ color: {SUCCESS}; }}
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
    st.markdown(
        f'<div class="status-banner {kind}">{text}</div>',
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

    # Main Metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        variant = ""
        if recommendation == "recommend_approval":
            variant = "success"
        elif recommendation == "recommend_rejection":
            variant = "danger"
        elif recommendation == "manual_review_required":
            variant = "warn"

        metric_card(
            "AI Recommendation",
            recommendation.replace("_", " ").title(),
            variant,
        )

    with col2:
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

    with col3:
        score = prediction.get("risk_score")
        metric_card(
            "Risk Score",
            str(score) if score is not None else "Not available",
        )

    st.write("")

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

    # Executive Summary
    section_title("Executive Summary")
    st.write(
        report.get(
            "executive_summary",
            "No report summary was returned.",
        )
    )

    # Risk Factors / Missing / Findings
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

    # Limitations
    limitations = report.get("limitations") or []
    if limitations:
        with st.expander("Report Limitations"):
            for item in limitations:
                st.write(f"• {item}")

    # Policy Assessment
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

    # Evidence Records
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

    # Debug
    with st.expander("Raw API Response"):
        st.json(result)


# ==========================================
# 6. SIDEBAR NAVIGATION
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
    )

    st.divider()

    st.markdown(
        '<div class="sidebar-meta">Internal Banking Decision Support<br>'
        'Credigo MVP v1.0</div>',
        unsafe_allow_html=True,
    )

    st.write("")

    if st.button("Test Backend Connection", use_container_width=True):
        try:
            result = check_health()
            st.success(f"Backend Connected: {result}")
        except ApiError as e:
            st.error(str(e))


# ==========================================
# 7. DASHBOARD PAGE
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
        metric_card("Investigation Engine", "LangGraph")

    with col3:
        metric_card("Risk Model", "Random Forest")

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
# 8. CUSTOMER SEARCH PAGE
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

    # Search Form
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

    # Search Logic
    if search_submitted:

        st.session_state.pop("credigo_customer", None)
        st.session_state.pop("credigo_customer_error", None)
        st.session_state.pop("credigo_customer_not_found", None)

        if (
            len(national_id_input) != 13
            or not national_id_input.isdigit()
        ):
            st.session_state["credigo_customer_error"] = (
                "National ID must contain exactly 13 digits."
            )
        else:
            try:
                with st.spinner("Searching customer..."):
                    customer = search_customer(national_id_input)
                st.session_state["credigo_customer"] = customer

            except ApiError as exc:
                if exc.status == 404:
                    st.session_state["credigo_customer_not_found"] = True
                else:
                    st.session_state["credigo_customer_error"] = str(exc)
            except Exception as exc:
                st.session_state["credigo_customer_error"] = str(exc)

    # Display Errors
    customer_error = st.session_state.get("credigo_customer_error")
    if customer_error:
        st.error(customer_error)

    if st.session_state.get("credigo_customer_not_found"):
        st.warning(
            "Customer not found. Please verify the National ID "
            "or check whether the customer has been registered."
        )

    # ======================================
    # CUSTOMER PROFILE
    # ======================================

    customer = st.session_state.get("credigo_customer")

    if customer:

        st.write("")

        status_banner("Customer successfully retrieved.", "success")

        section_title("Customer Profile")

        # Data extraction
        customer_id = str(customer.get("customer_id", "N/A"))
        first_name = str(customer.get("first_name", "N/A"))
        last_name = str(customer.get("last_name", "N/A"))
        date_of_birth = str(customer.get("date_of_birth", "N/A"))

        # Initials for avatar
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

        # Profile layout
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
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Store selected customer
        st.session_state["credigo_selected_customer_id"] = customer_id

        # Next Step
        section_title("Next Step")

        st.write(
            "The customer record has been retrieved. You may proceed "
            "to Credit Investigation to run the full risk assessment."
        )

        if st.button(
            "Continue to Credit Investigation",
            type="primary",
            use_container_width=True,
        ):
            st.session_state["credigo_go_to_investigation"] = True
            st.rerun()


# ==========================================
# 9. CREDIT INVESTIGATION PAGE
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

    selected_customer_id = st.session_state.get(
        "credigo_selected_customer_id", ""
    )

    if selected_customer_id:
        status_banner(
            f"Selected Customer ID: {selected_customer_id}",
            "success",
        )

    with st.form("investigation_form"):

        customer_id = st.text_input(
            "Customer ID (UUID)",
            value=selected_customer_id,
            placeholder="Enter customer UUID",
        ).strip()

        application_id = st.text_input(
            "Loan Application ID (UUID)",
            placeholder="Enter application UUID",
        ).strip()

        submitted = st.form_submit_button(
            "Start Investigation",
            type="primary",
            use_container_width=True,
        )

    if submitted:

        if not customer_id or not application_id:
            st.error(
                "Please enter both Customer ID and Application ID."
            )
        else:
            try:
                with st.spinner(
                    "Investigation is running. "
                    "This may take a few minutes..."
                ):
                    result = run_investigation(
                        customer_id,
                        application_id,
                    )

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
# 10. NAVIGATION FROM CUSTOMER SEARCH
# ==========================================

if st.session_state.pop("credigo_go_to_investigation", False):
    st.session_state["credigo_last_result"] = None
    st.session_state.pop("credigo_last_error", None)
    st.rerun()