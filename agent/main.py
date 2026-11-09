from uuid import UUID
from agent.graph import graph


def run_investigation(customer_id: str):

    initial_state = {
        "customer_id": UUID(customer_id)
    }

    result = graph.invoke(initial_state)

    return result


if __name__ == "__main__":

    customer_id = "047ac8e2-e93e-47b5-b12d-ca437d2695d0"

    result = run_investigation(customer_id)

    print("\n===== CREDIGO INVESTIGATION RESULT =====")

    print(result)