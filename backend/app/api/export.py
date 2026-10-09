import csv
import io
import uuid
from datetime import date
from decimal import Decimal
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.repositories.transaction_repository import TransactionRepository
from app.services.export_service import ExportService

router = APIRouter(prefix="/export", tags=["export"])


def csv_safe(value):
    if isinstance(value, str) and value[:1] in {"=", "+", "-", "@"}:
        return "'" + value
    return value


def get_export_service(db: Session = Depends(get_db)) -> ExportService:
    return ExportService(TransactionRepository(db))


@router.get("/transactions")
def export_transactions(
    format: Literal["csv"] = Query(default="csv"),
    date_from: date | None = None,
    date_to: date | None = None,
    account_id: uuid.UUID | None = None,
    category_id: uuid.UUID | None = None,
    transaction_type: Literal["income", "expense", "transfer"] | None = Query(default=None, alias="type"),
    min_amount: Decimal | None = Query(default=None, gt=0),
    max_amount: Decimal | None = Query(default=None, gt=0),
    description: str | None = None,
    current_user: User = Depends(get_current_user),
    service: ExportService = Depends(get_export_service),
):
    if date_from is not None and date_to is not None and date_from > date_to:
        raise HTTPException(status_code=422, detail="date_from no puede ser posterior a date_to")
    if min_amount is not None and max_amount is not None and min_amount > max_amount:
        raise HTTPException(status_code=422, detail="min_amount no puede ser mayor que max_amount")
    items = service.transactions(
        current_user.id, date_from=date_from, date_to=date_to,
        account_id=account_id, category_id=category_id,
        transaction_type=transaction_type, min_amount=min_amount,
        max_amount=max_amount, description=description,
    )

    def rows():
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["id", "account_id", "destination_account_id", "category_id", "type", "amount", "description", "transaction_date"])
        yield output.getvalue()
        for item in items:
            output = io.StringIO()
            csv.writer(output).writerow([
                item.id, item.account_id, item.destination_account_id, item.category_id,
                csv_safe(item.type), csv_safe(item.amount), csv_safe(item.description or ""), item.transaction_date,
            ])
            yield output.getvalue()

    return StreamingResponse(rows(), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=transactions.csv"})