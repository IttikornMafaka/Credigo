from app.database.connection import Base
from app.model.session import Customer,Account,Credit,Employment,Loan,Repayment

print("Models imported successfully!")

for table_name in Base.metadata.tables:
    print(table_name)

print("Total Tables:", len(Base.metadata.tables))