
import json
from uuid import UUID

from backend.dependence.database import get_db
from backend.services.policy_service import run_policy_assessment


application_id = UUID(
    "140ca4ca-87b0-43bc-8ff2-2196c03ace1d"
)

# National ID ของลูกค้าทดสอบ
national_id = "1101700000081"


db_generator = get_db()
db = next(db_generator)

try:
    result = run_policy_assessment(
        db=db,
        national_id=national_id,
        application_id=application_id
    )

    # 1. Review Information
    print("\n--- REVIEW INFORMATION ---")
    print("Manual Review:", result["manual_review_required"])
    print("Review Reasons:", result["review_reasons"])

    # 2. Policy Summary
    print("\n--- POLICY SUMMARY ---")

    for key, value in result["policy_summary"].items():
        print(f"{key}: {value}")

    # 3. Individual Policy Results
    print("\n--- POLICY RESULTS ---")

    for item in result["policy_results"]:
        policy_name = item.get("check", item.get("policy"))

        print(f"{policy_name}: {item['status']}")

    # 4. Full Policy Evidence
    print("\n--- FULL POLICY EVIDENCE ---")

    print(
        json.dumps(
            result["policy_results"],
            indent=2,
            ensure_ascii=False,
            default=str
        )
    )
    print("\n--- NORMALIZED EVIDENCE RECORDS ---")

    print(
        json.dumps(
            result["evidence_records"],
            indent=2,
            ensure_ascii=False,
            default=str
        )
    )

finally:
    db_generator.close()
