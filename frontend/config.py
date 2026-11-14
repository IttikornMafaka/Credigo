"""Central configuration for Credigo frontend. No secrets here."""
import os

# ── API ─────────────────────────────────────────────
API_BASE_URL = "http://127.0.0.1:8000"
REQUEST_TIMEOUT = 30  # seconds

# ── Design tokens ───────────────────────────────────
COLORS = {
    "navy":    "#14243A",
    "blue":    "#2563EB",
    "bg":      "#F5F7FA",
    "card":    "#FFFFFF",
    "success": "#16A34A",
    "warning": "#D97706",
    "danger":  "#DC2626",
    "muted":   "#64748B",
    "border":  "#E2E8F0",
}

FONTS = {"sans": "Inter, system-ui, sans-serif"}

# ── Enums / status maps ────────────────────────────
POLICY_STATUS_COLORS = {
    "PASS":         COLORS["success"],
    "FAIL":         COLORS["danger"],
    "UNVERIFIED":   COLORS["warning"],
    "NOT_REQUIRED": COLORS["muted"],
}

RECOMMENDATION_LABELS = {
    "recommend_approval":     ("Recommend Approval",     COLORS["success"]),
    "recommend_rejection":    ("Recommend Rejection",    COLORS["danger"]),
    "manual_review_required": ("Manual Review Required", COLORS["warning"]),
}

RISK_LEVEL_COLORS = {
    "LOW":     COLORS["success"],
    "MEDIUM":  COLORS["warning"],
    "HIGH":    COLORS["danger"],
    "UNKNOWN": COLORS["muted"],
}

# ── Investigation pipeline (LangGraph steps) ───────
# TODO: verify order/names against LangGraph state schema
INVESTIGATION_STEPS = [
    "Customer Retrieval",
    "Data Validation",
    "ML Risk Prediction",
    "Credit Policy Retrieval",
    "AI Analysis",
    "Policy Assessment",
    "Evidence Aggregation",
    "Credit Risk Report Generation",
    "Report Validation",
]