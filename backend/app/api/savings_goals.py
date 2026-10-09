import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.repositories.savings_goal_repository import SavingsGoalRepository
from app.schemas.savings_goal import (
    SavingsGoalCreate,
    SavingsGoalOut,
    SavingsGoalProgress,
)
from app.services.savings_goal_service import SavingsGoalService

router = APIRouter(prefix="/goals", tags=["savings-goals"])


def get_goal_service(db: Session = Depends(get_db)) -> SavingsGoalService:
    return SavingsGoalService(SavingsGoalRepository(db))


@router.get("", response_model=list[SavingsGoalOut])
def list_goals(
    current_user: User = Depends(get_current_user),
    service: SavingsGoalService = Depends(get_goal_service),
):
    return service.list_goals(current_user.id)


@router.post("", response_model=SavingsGoalOut, status_code=status.HTTP_201_CREATED)
def create_goal(
    data: SavingsGoalCreate,
    current_user: User = Depends(get_current_user),
    service: SavingsGoalService = Depends(get_goal_service),
):
    return service.create_goal(current_user.id, data)


@router.post("/{goal_id}/progress", response_model=SavingsGoalOut)
def update_goal_progress(
    goal_id: uuid.UUID,
    data: SavingsGoalProgress,
    current_user: User = Depends(get_current_user),
    service: SavingsGoalService = Depends(get_goal_service),
):
    try:
        goal = service.update_progress(current_user.id, goal_id, data.current_amount)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    if goal is None:
        raise HTTPException(status_code=404, detail="Meta no encontrada")
    return goal