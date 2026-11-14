from backend.dependence.database import get_db
from backend.services.policy_service import get_crp_041_evidence

national_id = "1101700000081"

db_generator = get_db()
db = next(db_generator)

try:
    result = get_crp_041_evidence(
        db=db,
        national_id=national_id
    )

    print("\n--- CRP-041 REPAYMENT EVIDENCE ---")

    for key, value in result.items():
        if key != "repayments":
            print(f"{key}: {value}")

    print("\n--- REPAYMENT DETAILS ---")

    for item in result["repayments"]:
        print(item)

finally:
    db_generator.close()