from decimal import Decimal

from app.repositories.savings_goal_repository import SavingsGoalRepository
from app.schemas.savings_goal import SavingsGoalCreate


class SavingsGoalService:
    def __init__(self, repository: SavingsGoalRepository):
        self.repository = repository

    @staticmethod
    def _with_percentage(goal):
        result = {
            "id": goal.id,
            "name": goal.name,
            "target_amount": goal.target_amount,
            "current_amount": goal.current_amount,
            "target_date": goal.target_date,
            "percentage": min(
                Decimal("100"),
                (goal.current_amount / goal.target_amount) * Decimal("100"),
            ),
        }
        return result

    def list_goals(self, user_id):
        return [self._with_percentage(goal) for goal in self.repository.list_by_user(user_id)]

    def create_goal(self, user_id, data: SavingsGoalCreate):
        return self._with_percentage(self.repository.create(user_id, data))

    def update_progress(self, user_id, goal_id, current_amount):
        goal = self.repository.get_by_id(user_id, goal_id)
        if goal is None:
            return None
        if current_amount > goal.target_amount:
            raise ValueError("El avance no puede superar el monto objetivo")
        return self._with_percentage(
            self.repository.update_progress(user_id, goal, current_amount)
        )