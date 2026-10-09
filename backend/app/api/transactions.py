import uuid
from datetime import date
from decimal import Decimal
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.repositories.transaction_repository import TransactionRepository
from app.schemas.transaction import (
    TransactionCreate,
    TransactionOut,
    TransactionPage,
    TransactionUpdate,
)
from app.services.transaction_service import TransactionService

router = APIRouter(prefix="/transactions", tags=["transactions"])


def get_transaction_service(db: Session = Depends(get_db)) -> TransactionService:
    return TransactionService(TransactionRepository(db))


def handle_business_error(error: ValueError):
    raise HTTPException(status_code=400, detail=str(error)) from error


@router.get("/", response_model=TransactionPage)
def list_transactions(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    date_from: date | None = None,
    date_to: date | None = None,
    account_id: uuid.UUID | None = None,
    category_id: uuid.UUID | None = None,
    transaction_type: Literal["income", "expense", "transfer"] | None = Query(
        default=None, alias="type"
    ),
    min_amount: Decimal | None = Query(default=None, gt=0),
    max_amount: Decimal | None = Query(default=None, gt=0),
    description: str | None = None,
    current_user: User = Depends(get_current_user),
    service: TransactionService = Depends(get_transaction_service),
):
    if date_from is not None and date_to is not None and date_from > date_to:
        raise HTTPException(
            status_code=422, detail="date_from no puede ser posterior a date_to"
        )
    if min_amount is not None and max_amount is not None and min_amount > max_amount:
        raise HTTPException(
            status_code=422, detail="min_amount no puede ser mayor que max_amount"
        )
    return service.list_transactions(
        current_user.id,
        page=page,
        page_size=page_size,
        date_from=date_from,
        date_to=date_to,
        account_id=account_id,
        category_id=category_id,
        transaction_type=transaction_type,
        min_amount=min_amount,
        max_amount=max_amount,
        description=description,
    )


@router.post("/", response_model=TransactionOut, status_code=status.HTTP_201_CREATED)
def create_transaction(
    data: TransactionCreate,
    current_user: User = Depends(get_current_user),
    service: TransactionService = Depends(get_transaction_service),
):
    try:
        return service.create_transaction(current_user.id, data)
    except ValueError as error:
        handle_business_error(error)


@router.get("/{transaction_id}", response_model=TransactionOut)
def get_transaction(
    transaction_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: TransactionService = Depends(get_transaction_service),
):
    transaction = service.get_transaction(current_user.id, transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return transaction


@router.put("/{transaction_id}", response_model=TransactionOut)
def update_transaction(
    transaction_id: uuid.UUID,
    data: TransactionUpdate,
    current_user: User = Depends(get_current_user),
    service: TransactionService = Depends(get_transaction_service),
):
    try:
        transaction = service.update_transaction(current_user.id, transaction_id, data)
    except ValueError as error:
        handle_business_error(error)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return transaction


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(
    transaction_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: TransactionService = Depends(get_transaction_service),
):
    try:
        deleted = service.delete_transaction(current_user.id, transaction_id)
    except ValueError as error:
        handle_business_error(error)
    if not deleted:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return Response(status_code=status.HTTP_204_NO_CONTENT)