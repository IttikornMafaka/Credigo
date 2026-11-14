
from typing import Literal
from pydantic import BaseModel, Field


class EvidenceReference(BaseModel):
    policy_id: str
    check_id: str
    status: str
    source: str | None = None


class RiskFactor(BaseModel):
    factor: str
    explanation: str
    severity: Literal["LOW", "MEDIUM", "HIGH","UNKNOWN"]
    evidence: list[EvidenceReference] = Field(default_factory=list)


class CreditRiskReport(BaseModel):
    recommendation: Literal[
        "recommend_approval",
        "recommend_rejection",
        "manual_review_required"
    ]

    risk_level: Literal["LOW", "MEDIUM", "HIGH", "UNKNOWN"]

    executive_summary: str

    key_risk_factors: list[RiskFactor] = Field(
        default_factory=list
    )

    verified_findings: list[str] = Field(
        default_factory=list
    )

    missing_information: list[str] = Field(
        default_factory=list
    )

    limitations: list[str] = Field(
        default_factory=list
    )
