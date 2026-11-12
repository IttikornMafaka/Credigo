import json
from uuid import UUID

from agent.nodes import validation_node

state = {
    "customer_id": UUID(
        "047ac8e2-e93e-47b5-b12d-ca437d2695d0"
    ),
    "customer_data": {
        "national_id": "1101700000081"
    },
    "evidence": []
}

result = validation_node(state)

print(
    json.dumps(
        result,
        indent=2,
        ensure_ascii=False,
        default=str
    )
)