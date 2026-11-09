from typing import Any
from agent.state import InvestigationState
from uuid import UUID
from backend.dependence.database import SessionLocal
from backend.services import customers_service
from backend.services.prediction_service import predict_credit_risk

# 1. Retrieve Customer Node ค้นหาลูกค้าจาก UUID

def retrieve_customer_node(state:InvestigationState) -> dict[str,Any] : 
    customer_id = state["customer_id"]
    db = SessionLocal()
    try : 
        customer = customers_service.get_customer_by_id(db=db,customer_id=customer_id)
        if customer is None : 
            return {"customer_data":{},"status":"customer_not_found","error":"Customer not found"}
        customer_data = {
            "customer_id": UUID(str(customer.customer_id)) ,
            "national_id" : str(customer.national_id)
        }
        return {
            "customer_data":customer_data ,
            "status" : "customer_retrieved",
            "error": ""
        }
    finally : 
        db.close()
        
        
# 2. Validation Node ตรวจสอบข้อมูลลูกค้า

def validation_node(state: InvestigationState) -> dict[str, Any]:
    
    customer_data = state.get("customer_data", {})

    if not customer_data:
        return {
            "validation_result": {
                "status": "NEEDS_REVIEW",
                "message": "Customer data not found"
            },
            "status": "validation_failed"
        }

    return {
        "validation_result": {
            "status": "PASS",
            "message": "Validation service integration required"
        },
        "status": "validation_passed"
    }
    
# 3. Prediction Node

def prediction_node(state: InvestigationState) -> dict[str, Any]:
    
    customer_data = state.get("customer_data", {})

    if not customer_data:
        return {
            "ml_prediction": {},
            "status": "prediction_failed",
            "error": "Customer data not found"
        }

    national_id = customer_data.get("national_id")

    if not national_id:
        return {
            "ml_prediction": {},
            "status": "prediction_failed",
            "error": "National ID not found"
        }

    db = SessionLocal()

    try:
        prediction = predict_credit_risk(
            db=db,
            national_id=national_id
        )

        return {
            "ml_prediction": prediction,
            "status": "prediction_completed",
            "error": ""
        }

    except Exception as e:
        return {
            "ml_prediction": {},
            "status": "prediction_failed",
            "error": str(e)
        }

    finally:
        db.close()
        
# 4. Policy Retrieval Node

def policy_retrieval_node(state:InvestigationState) -> dict[str,Any] : 
    return {
        "retrieved_policies": [] ,
        "status" : "policy_retrieval_pending"
    }
    
# 5. Analysis Node

def analysis_node(state:InvestigationState) -> dict[str,Any] :
    customer_data = state.get("customer_data",{})
    ml_prediction = state.get("ml_prediction",{})
    retrieved_policies = state.get("retrieved_policies",[])
    
    return {
        "policy_analysis" : {
            "customer_data_available": bool(customer_data),
            "ml_prediction_available": bool(ml_prediction),
            "policy_documents_found": len(retrieved_policies)
        },
        "ai_recommendation":"manual_review_required",
        "status":"analysis_placeholder_completed"
    }
    
# 6. Reflection Node

def reflection_node(state:InvestigationState) -> dict[str,Any] : 
    policy_analysis = state.get("policy_analysis", {})
    evidence = state.get("evidence", [])
    
    if not policy_analysis or not evidence:
        return {
            "ai_recommendation": "manual_review_required",
            "status": "reflection_requires_review"
        }

    return {
        "status": "reflection_completed"
    }
