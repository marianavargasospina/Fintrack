import uuid

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.repositories.budget_repository import BudgetRepository
from app.schemas.budget import BudgetCreate, BudgetOut, BudgetProgress, BudgetUpdate
from app.services.budget_service import BudgetService

router = APIRouter(prefix="/budgets", tags=["budgets"])


def get_budget_service(db: Session = Depends(get_db)) -> BudgetService:
    return BudgetService(BudgetRepository(db))


def raise_business_error(error: ValueError):
    raise HTTPException(status_code=400, detail=str(error)) from error


@router.get("/", response_model=list[BudgetOut])
def list_budgets(
    current_user: User = Depends(get_current_user),
    service: BudgetService = Depends(get_budget_service),
):
    return service.list_budgets(current_user.id)


@router.post("/", response_model=BudgetOut, status_code=status.HTTP_201_CREATED)
def create_budget(
    data: BudgetCreate,
    current_user: User = Depends(get_current_user),
    service: BudgetService = Depends(get_budget_service),
):
    try:
        return service.create_budget(current_user.id, data)
    except ValueError as error:
        raise_business_error(error)


@router.get("/{budget_id}", response_model=BudgetOut)
def get_budget(
    budget_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: BudgetService = Depends(get_budget_service),
):
    budget = service.get_budget(current_user.id, budget_id)
    if budget is None:
        raise HTTPException(status_code=404, detail="Presupuesto no encontrado")
    return budget


@router.get("/{budget_id}/progress", response_model=BudgetProgress)
def get_budget_progress(
    budget_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: BudgetService = Depends(get_budget_service),
):
    progress = service.progress(current_user.id, budget_id)
    if progress is None:
        raise HTTPException(status_code=404, detail="Presupuesto no encontrado")
    return progress


@router.put("/{budget_id}", response_model=BudgetOut)
def update_budget(
    budget_id: uuid.UUID,
    data: BudgetUpdate,
    current_user: User = Depends(get_current_user),
    service: BudgetService = Depends(get_budget_service),
):
    try:
        budget = service.update_budget(current_user.id, budget_id, data)
    except ValueError as error:
        raise_business_error(error)
    if budget is None:
        raise HTTPException(status_code=404, detail="Presupuesto no encontrado")
    return budget


@router.delete("/{budget_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_budget(
    budget_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: BudgetService = Depends(get_budget_service),
):
    deleted = service.delete_budget(current_user.id, budget_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Presupuesto no encontrado")
    return Response(status_code=status.HTTP_204_NO_CONTENT)