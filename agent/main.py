
from uuid import UUID
from agent.graph import graph


def run_investigation(customer_id: str,application_id: str):

    # 1. Validate UUID
    try:
        customer_uuid = UUID(customer_id)
        application_uuid = UUID(application_id)

    except ValueError:
        raise ValueError("Invalid customer_id or application_id")

    # 2. Create Initial State
    initial_state = {
        "customer_id": customer_uuid,
        "application_id": application_uuid,
        "retry_count": 0,
        "max_retries": 2
    }

    # 3. Execute LangGraph
    result = graph.invoke(initial_state)

    # 4. Return Result
    return result
