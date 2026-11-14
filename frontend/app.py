import streamlit as st
import requests
from datetime import datetime

# =====================================
# 1. PAGE CONFIGURATION
# =====================================

st.set_page_config(
    page_title="Credigo | Credit Risk Intelligence",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_BASE_URL = "http://127.0.0.1:8000"


# =====================================
# 2. CUSTOM CSS
# =====================================

st.markdown("""
<style>

    .stApp {
        background-color: #F5F7FA;
    }

    [data-testid="stSidebar"] {
        background-color: #14243A;
    }

    [data-testid="stSidebar"] * {
        color: white;
    }

    .main-title {
        font-size: 32px;
        font-weight: 700;
        color: #14243A;
        margin-bottom: 0px;
    }

    .subtitle {
        color: #64748B;
        font-size: 14px;
        margin-bottom: 25px;
    }

    .metric-card {
        background-color: white;
        padding: 22px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        min-height: 125px;
    }

    .metric-label {
        color: #64748B;
        font-size: 14px;
    }

    .metric-value {
        color: #14243A;
        font-size: 25px;
        font-weight: 700;
        margin-top: 10px;
    }

    .section-title {
        color: #14243A;
        font-size: 20px;
        font-weight: 650;
        margin-top: 20px;
    }

    .status-online {
        color: #15803D;
        font-weight: 700;
    }

    .status-offline {
        color: #DC2626;
        font-weight: 700;
    }

</style>
""", unsafe_allow_html=True)


# =====================================
# 3. SIDEBAR
# =====================================

with st.sidebar:

    st.title("🏦 CREDIGO")

    st.caption("Credit Risk Intelligence System")

    st.divider()

    page = st.radio(
        "MAIN MENU",
        [
            "Dashboard",
            "Customer Search",
            "Loan Applications",
            "Credit Investigation",
            "Credit Risk Report",
            "Evidence & Policy Review"
        ]
    )

    st.divider()

    st.caption("INTERNAL BANKING SYSTEM")
    st.caption("Credigo MVP v1.0")


# =====================================
# 4. API HEALTH CHECK
# =====================================

def check_api_health():

    try:

        response = requests.get(
            f"{API_BASE_URL}/health",
            timeout=5
        )

        response.raise_for_status()

        return True

    except requests.RequestException:

        return False


api_online = check_api_health()


# =====================================
# 5. DASHBOARD HEADER
# =====================================

if page == "Dashboard":

    st.markdown(
        '<div class="main-title">Credit Risk Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Monitor the Credigo credit investigation system and AI workflow.'
        '</div>',
        unsafe_allow_html=True
    )

    # ---------------------------------
    # System Status
    # ---------------------------------

    st.markdown("### System Overview")

    col1, col2, col3 = st.columns(3)

    with col1:

        status = "Online" if api_online else "Offline"

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Backend API</div>
                <div class="metric-value">{status}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">AI Investigation Engine</div>
                <div class="metric-value">LangGraph</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">ML Model</div>
                <div class="metric-value">Random Forest</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    if api_online:

        st.success("Credigo Backend API is responding normally.")

    else:

        st.error(
            "Cannot connect to Credigo Backend. "
            "Please start the FastAPI server."
        )

    # ---------------------------------
    # Investigation Workflow
    # ---------------------------------

    st.markdown(
        '<div class="section-title">Investigation Workflow</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "The AI-powered credit risk investigation pipeline."
    )

    workflow = [
        ("01", "Customer Retrieval", "Retrieve customer information"),
        ("02", "Data Validation", "Validate customer and financial data"),
        ("03", "ML Risk Prediction", "Predict credit default probability"),
        ("04", "Policy Retrieval", "Retrieve relevant credit policies"),
        ("05", "AI Analysis", "Analyze evidence using LLM"),
        ("06", "Policy Assessment", "Evaluate deterministic policy rules"),
        ("07", "Evidence Aggregation", "Collect verified and missing evidence"),
        ("08", "Risk Report", "Generate and validate credit risk report")
    ]

    for number, title, description in workflow:

        col1, col2 = st.columns([1, 8])

        with col1:

            st.markdown(f"### {number}")

        with col2:

            st.markdown(f"**{title}**")
            st.caption(description)

    st.divider()

    # ---------------------------------
    # Quick Actions
    # ---------------------------------

    st.markdown(
        '<div class="section-title">Quick Actions</div>',
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🔍 Start Credit Investigation",
            use_container_width=True
        ):

            st.session_state["selected_page"] = "Credit Investigation"
            st.rerun()

    with col2:

        if st.button(
            "👤 Search Customer",
            use_container_width=True
        ):

            st.session_state["selected_page"] = "Customer Search"
            st.rerun()

    st.divider()

    st.caption(
        f"Last page refresh: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )


# =====================================
# 6. OTHER PAGES - PLACEHOLDERS
# =====================================

else:

    st.title(page)

    st.info(
        f"The {page} module will be implemented in the next development step."
    )