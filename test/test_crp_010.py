
from backend.dependence.database import SessionLocal
from backend.services.policy_service import check_crp_010

db = SessionLocal()

try:
    result = check_crp_010(
        db=db,
        national_id="1101700000081"
    )

    print("--- CRP-010 POLICY DECISION ---")
    print("Policy:", result["policy"])
    print("Status:", result["status"])
    print("Basic Data:", result["basic_data_status"])
    print("Reason:", result["reason"])

    print("\n--- EVIDENCE ---")

    for key, value in result["evidence"].items():
        print(f"{key}: {value}")

finally:
    db.close()
