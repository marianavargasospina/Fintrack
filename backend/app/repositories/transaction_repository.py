import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import func, or_, select, text
from sqlalchemy.orm import Session

from app.models.account import Account
from app.models.category import Category
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate


class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def _set_user_context(self, user_id) -> None:
        self.db.execute(
            text("SELECT set_config('app.current_user_id', :uid, true)"),
            {"uid": str(user_id)},
        )

    def get_account(self, user_id, account_id) -> Account | None:
        self._set_user_context(user_id)
        return (
            self.db.query(Account)
            .filter(Account.id == account_id, Account.user_id == user_id)
            .first()
        )

    def get_category(self, user_id, category_id) -> Category | None:
        self._set_user_context(user_id)
        return (
            self.db.query(Category)
            .filter(Category.id == category_id, Category.user_id == user_id)
            .first()
        )

    def get_by_id(self, user_id, transaction_id) -> Transaction | None:
        self._set_user_context(user_id)
        return (
            self.db.query(Transaction)
            .filter(Transaction.id == transaction_id, Transaction.user_id == user_id)
            .first()
        )

    def list_by_user(
        self,
        user_id,
        page: int,
        page_size: int,
        date_from: date | None = None,
        date_to: date | None = None,
        account_id: uuid.UUID | None = None,
        category_id: uuid.UUID | None = None,
        transaction_type: str | None = None,
        min_amount: Decimal | None = None,
        max_amount: Decimal | None = None,
        description: str | None = None,
    ) -> tuple[list[Transaction], int]:
        self._set_user_context(user_id)
        query = self.db.query(Transaction).filter(Transaction.user_id == user_id)
        if date_from is not None:
            query = query.filter(Transaction.transaction_date >= date_from)
        if date_to is not None:
            query = query.filter(Transaction.transaction_date <= date_to)
        if account_id is not None:
            query = query.filter(
                or_(
                    Transaction.account_id == account_id,
                    Transaction.destination_account_id == account_id,
                )
            )
        if category_id is not None:
            query = query.filter(Transaction.category_id == category_id)
        if transaction_type is not None:
            query = query.filter(Transaction.type == transaction_type)
        if min_amount is not None:
            query = query.filter(Transaction.amount >= min_amount)
        if max_amount is not None:
            query = query.filter(Transaction.amount <= max_amount)
        if description is not None:
            query = query.filter(Transaction.description.ilike(f"%{description}%"))

        total = query.with_entities(func.count(Transaction.id)).scalar() or 0
        items = (
            query.order_by(Transaction.transaction_date.desc(), Transaction.id.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )
        return items, total

    def _locked_accounts(self, user_id, account_ids: set[uuid.UUID]) -> dict:
        self._set_user_context(user_id)
        accounts = (
            self.db.query(Account)
            .filter(Account.user_id == user_id, Account.id.in_(account_ids))
            .order_by(Account.id)
            .with_for_update()
            .all()
        )
        return {account.id: account for account in accounts}

    @staticmethod
    def _apply_balance(account: Account, transaction_type: str, amount: Decimal, sign: int = 1):
        if transaction_type == "income":
            account.current_balance += amount * sign
        elif transaction_type == "expense":
            account.current_balance -= amount * sign
        else:
            account.current_balance -= amount * sign

    def _apply_effect(self, transaction: Transaction, accounts: dict, sign: int = 1):
        self._apply_balance(accounts[transaction.account_id], transaction.type, transaction.amount, sign)
        if transaction.type == "transfer":
            accounts[transaction.destination_account_id].current_balance += (
                transaction.amount * sign
            )

    def create(self, user_id, data: TransactionCreate) -> Transaction:
        account_ids = {data.account_id}
        if data.destination_account_id is not None:
            account_ids.add(data.destination_account_id)
        accounts = self._locked_accounts(user_id, account_ids)
        if len(accounts) != len(account_ids):
            raise ValueError("Una de las cuentas no pertenece al usuario")

        transaction = Transaction(user_id=user_id, **data.model_dump())
        self.db.add(transaction)
        self._apply_effect(transaction, accounts)
        self.db.flush()
        self.db.refresh(transaction)
        self.db.commit()
        return transaction

    def update(self, user_id, transaction_id, data: TransactionUpdate) -> Transaction | None:
        self._set_user_context(user_id)
        transaction = (
            self.db.query(Transaction)
            .filter(Transaction.id == transaction_id, Transaction.user_id == user_id)
            .with_for_update()
            .first()
        )
        if transaction is None:
            return None

        account_ids = {transaction.account_id, data.account_id}
        if transaction.destination_account_id is not None:
            account_ids.add(transaction.destination_account_id)
        if data.destination_account_id is not None:
            account_ids.add(data.destination_account_id)
        accounts = self._locked_accounts(user_id, account_ids)
        if len(accounts) != len(account_ids):
            raise ValueError("Una de las cuentas no pertenece al usuario")

        self._apply_effect(transaction, accounts, sign=-1)
        for field, value in data.model_dump().items():
            setattr(transaction, field, value)
        self._apply_effect(transaction, accounts)
        self.db.flush()
        self.db.refresh(transaction)
        self.db.commit()
        return transaction

    def delete(self, user_id, transaction_id) -> bool:
        self._set_user_context(user_id)
        transaction = (
            self.db.query(Transaction)
            .filter(Transaction.id == transaction_id, Transaction.user_id == user_id)
            .with_for_update()
            .first()
        )
        if transaction is None:
            return False

        account_ids = {transaction.account_id}
        if transaction.destination_account_id is not None:
            account_ids.add(transaction.destination_account_id)
        accounts = self._locked_accounts(user_id, account_ids)
        if len(accounts) != len(account_ids):
            raise ValueError("Una de las cuentas no pertenece al usuario")
        self._apply_effect(transaction, accounts, sign=-1)
        self.db.delete(transaction)
        self.db.commit()
        return True