from typing import TypedDict, Any
from uuid import UUID


class InvestigationState(TypedDict, total=False):

    # 1. Customer Information
    customer_id: UUID
    customer_data: dict[str, Any]

    # 2. Validation Result
    validation_result: dict[str, Any]

    # 3. Machine Learning Prediction
    ml_prediction: dict[str, Any]

    # 4. RAG Credit Policy
    retrieved_policies: list[dict[str, Any]]

    # 5. LLM Analysis
    policy_analysis: dict[str, Any]
    ai_recommend: str

    # 6. Evidence
    evidence: list[dict[str, Any]]

    # 7. Reflection
    reflection_result: dict[str, Any]
    reflection_feedback: str
    retry_count: int
    max_retries: int

    # 8. Report
    report_path: str

    # 9. Status
    status: str
    error: str