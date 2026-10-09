from datetime import date
from decimal import Decimal
from types import SimpleNamespace
from uuid import uuid4

from app.schemas.savings_goal import SavingsGoalCreate
from app.services.savings_goal_service import SavingsGoalService


class FakeGoalRepository:
    def __init__(self):
        self.goal = None

    def list_by_user(self, user_id):
        return [self.goal] if self.goal else []

    def create(self, user_id, data):
        self.goal = SimpleNamespace(id=uuid4(), **data.model_dump())
        return self.goal

    def get_by_id(self, user_id, goal_id):
        return self.goal if self.goal and self.goal.id == goal_id else None

    def update_progress(self, user_id, goal, current_amount):
        goal.current_amount = current_amount
        return goal


def test_create_goal_calculates_percentage():
    repository = FakeGoalRepository()
    service = SavingsGoalService(repository)
    goal = service.create_goal(uuid4(), SavingsGoalCreate(
        name="Emergency fund", target_amount=Decimal("1000"),
        current_amount=Decimal("250"), target_date=date(2027, 1, 1),
    ))
    assert goal["percentage"] == Decimal("25.00")


def test_progress_cannot_exceed_target():
    repository = FakeGoalRepository()
    service = SavingsGoalService(repository)
    goal = service.create_goal(uuid4(), SavingsGoalCreate(
        name="Trip", target_amount=Decimal("100"), target_date=date(2027, 1, 1),
    ))
    try:
        service.update_progress(uuid4(), goal["id"], Decimal("101"))
    except ValueError as error:
        assert "superar" in str(error)
    else:
        raise AssertionError("Expected a validation error")
