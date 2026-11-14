from backend.dependence.database import get_db
from backend.services.policy_service import check_crp_041

national_id = "1101700000081"

db_generator = get_db()
db = next(db_generator)

try:
    result = check_crp_041(
        db=db,
        national_id=national_id
    )

    print("\n--- CRP-041 POLICY DECISION ---")
    print("Policy:", result["policy"])
    print("Status:", result["status"])
    print("Reason:", result["reason"])

    print("\n--- EVIDENCE ---")

    for key, value in result["evidence"].items():
        print(f"{key}: {value}")

finally:
    db_generator.close()