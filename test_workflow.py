from uuid import UUID
import json

from agent.graph import graph

customer_id = UUID(
    "047ac8e2-e93e-47b5-b12d-ca437d2695d0"
)

initial_state = {
    "customer_id": customer_id,
    "retry_count": 0,
    "max_retries": 2,
    "evidence": []
}

result = graph.invoke(initial_state)

print(json.dumps(
    result,
    indent=2,
    ensure_ascii=False,
    default=str
))