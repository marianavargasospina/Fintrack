from sqlalchemy import or_, text
from sqlalchemy.orm import Session

from app.models.account import Account
from app.models.transaction import Transaction
from app.schemas.account import AccountCreate


class AccountRepository:
    def __init__(self, db: Session):
        self.db = db

    def _set_user_context(self, user_id) -> None:
        self.db.execute(
            text("SELECT set_config('app.current_user_id', :uid, true)"),
            {"uid": str(user_id)},
        )

    def list_by_user(self, user_id) -> list[Account]:
        self._set_user_context(user_id)
        return self.db.query(Account).all()

    def create(self, user_id, data: AccountCreate) -> Account:
        self._set_user_context(user_id)
        account = Account(
            user_id=user_id,
            name=data.name,
            type=data.type,
            currency=data.currency,
            current_balance=data.initial_balance,
        )
        self.db.add(account)
        self.db.flush()
        self.db.refresh(account)
        self.db.commit()
        return account

    def delete(self, user_id, account_id) -> bool:
        self._set_user_context(user_id)
        account = (
            self.db.query(Account)
            .filter(Account.id == account_id, Account.user_id == user_id)
            .with_for_update()
            .first()
        )
        if account is None:
            return False

        has_transactions = (
            self.db.query(Transaction.id)
            .filter(
                Transaction.user_id == user_id,
                or_(
                    Transaction.account_id == account_id,
                    Transaction.destination_account_id == account_id,
                ),
            )
            .first()
            is not None
        )
        if has_transactions:
            raise ValueError(
                "No puedes eliminar una cuenta que tiene movimientos asociados."
            )

        self.db.delete(account)
        self.db.commit()
        return True