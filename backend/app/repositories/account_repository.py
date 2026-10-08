from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models.account import Account
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
        self.db.commit()
        self.db.refresh(account)
        return account