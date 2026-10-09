from decimal import Decimal

from sqlalchemy import func, text
from sqlalchemy.orm import Session

from app.models.budget import Budget
from app.models.category import Category
from app.models.transaction import Transaction
from app.schemas.budget import BudgetCreate, BudgetUpdate


class BudgetRepository:
    def __init__(self, db: Session):
        self.db = db

    def _set_user_context(self, user_id) -> None:
        self.db.execute(
            text("SELECT set_config('app.current_user_id', :uid, true)"),
            {"uid": str(user_id)},
        )

    def get_category(self, user_id, category_id) -> Category | None:
        self._set_user_context(user_id)
        return (
            self.db.query(Category)
            .filter(Category.id == category_id, Category.user_id == user_id)
            .first()
        )

    def list_by_user(self, user_id) -> list[Budget]:
        self._set_user_context(user_id)
        return self.db.query(Budget).filter(Budget.user_id == user_id).all()

    def get_by_id(self, user_id, budget_id) -> Budget | None:
        self._set_user_context(user_id)
        return (
            self.db.query(Budget)
            .filter(Budget.id == budget_id, Budget.user_id == user_id)
            .first()
        )

    def create(self, user_id, data: BudgetCreate) -> Budget:
        self._set_user_context(user_id)
        budget = Budget(user_id=user_id, **data.model_dump())
        self.db.add(budget)
        self.db.flush()
        self.db.refresh(budget)
        self.db.commit()
        return budget

    def update(self, user_id, budget: Budget, data: BudgetUpdate) -> Budget:
        self._set_user_context(user_id)
        for field, value in data.model_dump().items():
            setattr(budget, field, value)
        self.db.flush()
        self.db.refresh(budget)
        self.db.commit()
        return budget

    def delete(self, user_id, budget: Budget) -> None:
        self._set_user_context(user_id)
        self.db.delete(budget)
        self.db.commit()

    def spent_for_budget(self, user_id, budget: Budget) -> Decimal:
        self._set_user_context(user_id)
        spent = (
            self.db.query(func.coalesce(func.sum(Transaction.amount), 0))
            .filter(
                Transaction.user_id == user_id,
                Transaction.category_id == budget.category_id,
                Transaction.type == "expense",
                Transaction.transaction_date >= budget.start_date,
                Transaction.transaction_date <= budget.end_date,
            )
            .scalar()
        )
        return Decimal(str(spent or 0))