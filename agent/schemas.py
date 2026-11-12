from typing import Literal # ตัวแปรสามารถรับค่าได้เฉพาะค่าที่เราระบุไว้เท่านั้น
from pydantic import BaseModel, Field

class ReflectionResult(BaseModel):
    
    # Field หมายถึง ช่องข้อมูลหรือคุณสมบัติ (Attribute) ที่อยู่ภายในโครงสร้างข้อมูลหรือ Object
    is_consistent: bool = Field(
        description="Whether the analysis is consistent with the available evidence")

    issues: list[str] = Field(description="List of contradictions or unsupported claims")

    missing_information: list[str] = Field(description="Information required for a more reliable analysis")

    requires_manual_review: bool = Field(description="Whether human review is required")

    reasoning_summary: str = Field(description="Explanation of the reflection result")
 
   
class CreditAnalysisResult(BaseModel):
    
    risk_level: Literal["low","medium","high","unknown"] = Field(description="Overall credit risk level based on verified data.")

    risk_factors: list[str] = Field(description="Identified factors that increase or decrease credit risk.")

    policy_compliance: list[str] = Field(description="Credit policy requirements, their compliance status, and supporting policy references.")

    supporting_evidence: list[str] = Field(description="Evidence supporting the analysis. Include source and page references where available.")

    recommendation: Literal["recommend_approval","recommend_rejection","manual_review_required"] = Field(description="A bounded recommendation for the human credit officer. Never make the final lending decision.")

    reasoning_summary: str = Field(description="A concise explanation of the analysis based only on verified data and retrieved policies.")