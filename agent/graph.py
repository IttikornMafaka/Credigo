
from langgraph.graph import StateGraph, START, END

from agent.state import InvestigationState

from agent.nodes import (
    retrieve_customer_node,
    validation_node,
    prediction_node,
    policy_retrieval_node,
    analysis_node,
    reflection_node,
    evidence_aggregation_node,
    policy_assessment_node,
    evidence_builder_node,
    credit_risk_report_node,
    report_validation_node
)


# 1. Routing Functions

def route_after_retrieve(state: InvestigationState):

    if state.get("status") == "customer_not_found":
        return "end"

    return "validation"


def route_after_validation(state: InvestigationState):

    if state.get("status") == "validation_passed":
        return "prediction"

    return "end"


def route_after_prediction(state: InvestigationState):

    if state.get("status") != "prediction_completed":
        return "end"

    return "policy_retrieval"


def route_after_policy_retrieval(state: InvestigationState):

    if state.get("status") != "policy_retrieval_completed":
        return "end"

    return "evidence_aggregation"


def route_after_analysis(state: InvestigationState):

    status = state.get("status")
    policy_analysis = state.get("policy_analysis", {})

    if status == "analysis_failed" or not policy_analysis:
        return "end"

    return "reflection"


def route_after_reflection(state: InvestigationState):

    status = state.get("status")

    if status == "reflection_requires_revision":
        return "analysis"

    if status in [
        "reflection_completed",
        "reflection_requires_review"
    ]:
        return "policy_assessment"

    return "end"


def route_after_policy_assessment(state: InvestigationState):

    if state.get("status") != "policy_assessment_completed":
        return "end"

    return "evidence_builder"


def route_after_evidence_builder(state: InvestigationState):

    if state.get("status") != "evidence_context_created":
        return "end"

    return "credit_risk_report"


def route_after_credit_risk_report(state: InvestigationState):

    if state.get("status") != "credit_risk_report_completed":
        return "end"

    return "report_validation"


def route_after_report_validation(state: InvestigationState):

    if state.get("status") == "report_validation_completed":
        return "end"

    return "end"


# 2. Initialize State Graph

work = StateGraph(InvestigationState)


# 3. Register Existing Nodes

work.add_node("retrieve_customer", retrieve_customer_node)
work.add_node("validation", validation_node)
work.add_node("prediction", prediction_node)
work.add_node("policy_retrieval", policy_retrieval_node)
work.add_node("evidence_aggregation", evidence_aggregation_node)
work.add_node("analysis", analysis_node)
work.add_node("reflection", reflection_node)


# 4. Register New Credit Risk Nodes

work.add_node("policy_assessment", policy_assessment_node)
work.add_node("evidence_builder", evidence_builder_node)
work.add_node("credit_risk_report", credit_risk_report_node)
work.add_node("report_validation", report_validation_node)


# 5. Define Workflow Edges

work.add_edge(START, "retrieve_customer")


work.add_conditional_edges(
    "retrieve_customer",
    route_after_retrieve,
    {
        "validation": "validation",
        "end": END
    }
)


work.add_conditional_edges(
    "validation",
    route_after_validation,
    {
        "prediction": "prediction",
        "end": END
    }
)


work.add_conditional_edges(
    "prediction",
    route_after_prediction,
    {
        "policy_retrieval": "policy_retrieval",
        "end": END
    }
)


work.add_conditional_edges(
    "policy_retrieval",
    route_after_policy_retrieval,
    {
        "evidence_aggregation": "evidence_aggregation",
        "end": END
    }
)


work.add_edge(
    "evidence_aggregation",
    "analysis"
)


work.add_conditional_edges(
    "analysis",
    route_after_analysis,
    {
        "reflection": "reflection",
        "end": END
    }
)


# Reflection Loop

work.add_conditional_edges(
    "reflection",
    route_after_reflection,
    {
        "analysis": "analysis",
        "policy_assessment": "policy_assessment",
        "end": END
    }
)


# New Credit Risk Pipeline

work.add_conditional_edges(
    "policy_assessment",
    route_after_policy_assessment,
    {
        "evidence_builder": "evidence_builder",
        "end": END
    }
)


work.add_conditional_edges(
    "evidence_builder",
    route_after_evidence_builder,
    {
        "credit_risk_report": "credit_risk_report",
        "end": END
    }
)


work.add_conditional_edges(
    "credit_risk_report",
    route_after_credit_risk_report,
    {
        "report_validation": "report_validation",
        "end": END
    }
)


work.add_conditional_edges(
    "report_validation",
    route_after_report_validation,
    {
        "end": END
    }
)


# 6. Compile Graph

graph = work.compile()
