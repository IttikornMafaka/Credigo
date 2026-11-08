from app.database.connection import SessionLocal
from backend.services.feature_service import extract_customer_features

db = SessionLocal()

try:
    # ใช้ National ID ของลูกค้าทดสอบใน Database
    national_id = "1101700000001"

    features = extract_customer_features(
        db=db,
        national_id=national_id
    )

    print("\n===== CREDIGO FEATURE EXTRACTION =====")

    for key, value in features.items():
        print(f"{key}: {value}")

    print("\nTotal Features:", len(features))

finally:
    db.close()