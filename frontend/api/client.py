import requests

API_BASE_URL = "http://127.0.0.1:8000"


def run_investigation(customer_id: str, application_id: str):

    url = f"{API_BASE_URL}/api/investigations/run"

    payload = {
        "customer_id": customer_id,
        "application_id": application_id
    }

    response = requests.post(
        url,
        json=payload,
        timeout=120
    )

    response.raise_for_status()

    return response.json()