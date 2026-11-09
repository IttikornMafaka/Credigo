from langgraph.graph import StateGraph, START, END

from agent.state import InvestigationState
from agent.nodes import retrieve_customer_node,validation_node,prediction_node,policy_retrieval_node,analysis_node,reflection_node

def route_after_retrieve(state: InvestigationState):
    
    if state.get("status") == "customer_not_found":
        return "end"

    return "validation"


def route_after_validation(state: InvestigationState):

    validation = state.get("validation_result", {})

    if validation.get("status") != "PASS":
        return "end"

    return "prediction"


def route_after_prediction(state: InvestigationState):

    if state.get("status") != "prediction_completed":
        return "end"

    return "policy_retrieval"

work = StateGraph(InvestigationState) 

work.add_node("retrieve_customer", retrieve_customer_node)
work.add_node("validation", validation_node)
work.add_node("prediction", prediction_node)
work.add_node("policy_retrieval", policy_retrieval_node)
work.add_node("analysis", analysis_node)
work.add_node("reflection", reflection_node)

work.add_edge(START, "retrieve_customer")

work.add_conditional_edges("retrieve_customer",route_after_retrieve,{"validation": "validation","end": END})

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

work.add_edge("policy_retrieval", "analysis")
work.add_edge("analysis", "reflection")
work.add_edge("reflection", END)

graph = work.compile()