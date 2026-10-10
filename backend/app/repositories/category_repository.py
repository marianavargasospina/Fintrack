from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models.budget import Budget
from app.models.category import Category
from app.models.transaction import Transaction
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def _set_user_context(self, user_id) -> None:
        self.db.execute(
            text("SELECT set_config('app.current_user_id', :uid, true)"),
            {"uid": str(user_id)},
        )

    def list_by_user(self, user_id) -> list[Category]:
        self._set_user_context(user_id)
        return self.db.query(Category).filter(Category.user_id == user_id).all()

    def get_by_id(self, user_id, category_id) -> Category | None:
        self._set_user_context(user_id)
        return (
            self.db.query(Category)
            .filter(Category.id == category_id, Category.user_id == user_id)
            .first()
        )

    def create(self, user_id, data: CategoryCreate) -> Category:
        self._set_user_context(user_id)
        category = Category(user_id=user_id, name=data.name, type=data.type)
        self.db.add(category)
        self.db.flush()
        self.db.refresh(category)
        self.db.commit()
        return category

    def update(
        self, user_id, category: Category, data: CategoryUpdate
    ) -> Category:
        self._set_user_context(user_id)
        category.name = data.name
        category.type = data.type
        self.db.flush()
        self.db.refresh(category)
        self.db.commit()
        return category

    def delete(self, user_id, category: Category) -> None:
        self._set_user_context(user_id)
        has_transactions = (
            self.db.query(Transaction.id)
            .filter(
                Transaction.user_id == user_id,
                Transaction.category_id == category.id,
            )
            .first()
            is not None
        )
        if has_transactions:
            raise ValueError(
                "No puedes eliminar una categoría que tiene movimientos asociados."
            )

        has_budgets = (
            self.db.query(Budget.id)
            .filter(Budget.user_id == user_id, Budget.category_id == category.id)
            .first()
            is not None
        )
        if has_budgets:
            raise ValueError(
                "No puedes eliminar una categoría que tiene presupuestos asociados."
            )

        self.db.delete(category)
        self.db.commit()