from api import client

# ── VERIFIED (จาก spec) ─────────────────────────────
def run_investigation(customer_id: str, application_id: str) -> dict:
    return client.post("/api/investigations/run", {
        "customer_id": customer_id,
        "application_id": application_id,
    })

# ── TODO: ยืนยัน path + schema จาก openapi.json ─────
# def search_customers(query, limit=25):    return client.get("/api/customers", {"q": query, "limit": limit})
# def get_customer(customer_id):            return client.get(f"/api/customers/{customer_id}")
# def list_applications(filters=None):      return client.get("/api/loan-applications", filters)
# def get_application(app_id):              return client.get(f"/api/loan-applications/{app_id}")
# def list_risk_reports():                  return client.get("/api/credit-risk-reports")
# def health():                             return client.get("/api/health")
# def ml_status():                          return client.get("/api/ml/status")
# def llm_status():                         return client.get("/api/llm/status")