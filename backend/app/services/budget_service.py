from decimal import Decimal, ROUND_HALF_UP

from app.repositories.budget_repository import BudgetRepository
from app.schemas.budget import BudgetCreate, BudgetProgress, BudgetUpdate


class BudgetService:
    def __init__(self, repository: BudgetRepository):
        self.repository = repository

    def _validate_category(self, user_id, category_id):
        category = self.repository.get_category(user_id, category_id)
        if category is None:
            raise ValueError("La categoría no pertenece al usuario")
        if category.type != "expense":
            raise ValueError("Un presupuesto solo puede usar categorías de gasto")

    def list_budgets(self, user_id):
        return self.repository.list_by_user(user_id)

    def get_budget(self, user_id, budget_id):
        return self.repository.get_by_id(user_id, budget_id)

    def create_budget(self, user_id, data: BudgetCreate):
        self._validate_category(user_id, data.category_id)
        return self.repository.create(user_id, data)

    def update_budget(self, user_id, budget_id, data: BudgetUpdate):
        self._validate_category(user_id, data.category_id)
        budget = self.repository.get_by_id(user_id, budget_id)
        if budget is None:
            return None
        return self.repository.update(user_id, budget, data)

    def delete_budget(self, user_id, budget_id):
        budget = self.repository.get_by_id(user_id, budget_id)
        if budget is None:
            return False
        self.repository.delete(user_id, budget)
        return True

    def progress(self, user_id, budget_id):
        budget = self.repository.get_by_id(user_id, budget_id)
        if budget is None:
            return None
        spent = self.repository.spent_for_budget(user_id, budget)
        percentage = (spent / budget.amount_limit * 100).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        if percentage > 100:
            status = "exceeded"
        elif percentage >= 80:
            status = "warning"
        else:
            status = "ok"
        return BudgetProgress(
            budget_id=budget.id,
            category_id=budget.category_id,
            amount_limit=budget.amount_limit,
            start_date=budget.start_date,
            end_date=budget.end_date,
            spent=spent,
            percentage=percentage,
            status=status,
        )