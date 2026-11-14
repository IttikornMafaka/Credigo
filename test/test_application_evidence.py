from uuid import UUID

from backend.dependence.database import get_db
from backend.services.feature_service import extract_application_evidence

application_id = UUID(
    "140ca4ca-87b0-43bc-8ff2-2196c03ace1d"
)

db_generator = get_db()
db = next(db_generator)

try:
    evidence = extract_application_evidence(
        db=db,
        national_id="1101700000081",
        application_id=application_id
    )

    print("\n--- APPLICATION EVIDENCE ---")

    for key, value in evidence.items():
        print(f"{key}: {value}")

finally:
    db_generator.close()