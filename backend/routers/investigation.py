
from uuid import UUID
import logging
from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from agent.main import run_investigation


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/investigations",
    tags=["investigations"]
)


# 1. Request Schema
class InvestigationRequest(BaseModel):
    customer_id: UUID
    application_id: UUID


# 2. Run Investigation
@router.post("/run")
def create_investigation(
    request: InvestigationRequest
) -> dict[str, Any]:

    try:
        result = run_investigation(
            customer_id=str(request.customer_id),
            application_id=str(request.application_id)
        )

        # Return only information needed by the frontend
        response = {
            "customer_id": request.customer_id,
            "application_id": request.application_id,
            "status": result.get("status"),
            "ml_prediction": result.get("ml_prediction"),
            "ai_recommend": result.get("ai_recommend"),
            "credit_risk_report": result.get("credit_risk_report"),
            "policy_assessment": result.get("policy_assessment"),
            "evidence_context": result.get("evidence_context"),
            "error": result.get("error", "")
        }

        return jsonable_encoder(response)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception:
        logger.exception("Credigo investigation failed")

        raise HTTPException(
            status_code=500,
            detail="Investigation failed. Please try again later."
        )
