from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models.savings_goal import SavingsGoal
from app.schemas.savings_goal import SavingsGoalCreate


class SavingsGoalRepository:
    def __init__(self, db: Session):
        self.db = db

    def _set_user_context(self, user_id) -> None:
        self.db.execute(
            text("SELECT set_config('app.current_user_id', :uid, true)"),
            {"uid": str(user_id)},
        )

    def list_by_user(self, user_id) -> list[SavingsGoal]:
        self._set_user_context(user_id)
        return self.db.query(SavingsGoal).filter(SavingsGoal.user_id == user_id).all()

    def get_by_id(self, user_id, goal_id) -> SavingsGoal | None:
        self._set_user_context(user_id)
        return self.db.query(SavingsGoal).filter(
            SavingsGoal.id == goal_id, SavingsGoal.user_id == user_id
        ).first()

    def create(self, user_id, data: SavingsGoalCreate) -> SavingsGoal:
        self._set_user_context(user_id)
        goal = SavingsGoal(user_id=user_id, **data.model_dump())
        self.db.add(goal)
        self.db.flush()
        self.db.refresh(goal)
        self.db.commit()
        return goal

    def update_progress(self, user_id, goal: SavingsGoal, current_amount):
        self._set_user_context(user_id)
        goal.current_amount = current_amount
        self.db.flush()
        self.db.refresh(goal)
        self.db.commit()
        return goal

    def delete(self, user_id, goal: SavingsGoal) -> None:
        self._set_user_context(user_id)
        self.db.delete(goal)
        self.db.commit()