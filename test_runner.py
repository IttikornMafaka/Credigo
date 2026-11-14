
from agent.main import run_investigation


def test_run_investigation():

    customer_id = "047ac8e2-e93e-47b5-b12d-ca437d2695d0"

    application_id = "140ca4ca-87b0-43bc-8ff2-2196c03ace1d"

    result = run_investigation(
        customer_id=customer_id,
        application_id=application_id
    )

    assert isinstance(result, dict)

    assert "status" in result

    print("\n===== CREDIGO INVESTIGATION RESULT =====")

    print(result)
