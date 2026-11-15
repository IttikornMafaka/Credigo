from sqlalchemy.orm import Session
from app.model.session import Account, Customer


def get_account_by_customerID(db: Session, customer_id):
    return (
        db.query(Account)
        .filter(Account.customer_id == customer_id)
        .all()
    )


def create_account(db: Session, customer_id, account_data):

    customer = (
        db.query(Customer)
        .filter(Customer.customer_id == customer_id)
        .first()
    )

    if customer is None:
        return None

    account = Account(
        customer_id=customer_id,
        account_number=account_data.account_number,
        bank_name=account_data.bank_name,
        account_type=account_data.account_type,
        balance=account_data.balance,
        account_status=account_data.account_status,
        opened_at=account_data.opened_at,
    )

    try:
        db.add(account)
        db.commit()
        db.refresh(account)

        return account

    except Exception:
        db.rollback()
        raise