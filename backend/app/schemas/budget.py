import calendar
import uuid
from datetime import date
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


BudgetStatus = Literal["ok", "warning", "exceeded"]


class BudgetData(BaseModel):
    category_id: uuid.UUID
    amount_limit: Decimal = Field(gt=0)
    start_date: date
    end_date: date

    @model_validator(mode="after")
    def validate_month(self):
        if self.start_date.day != 1:
            raise ValueError("start_date debe ser el primer día del mes")
        last_day = calendar.monthrange(self.start_date.year, self.start_date.month)[1]
        expected_end = date(
            self.start_date.year, self.start_date.month, last_day
        )
        if self.end_date != expected_end:
            raise ValueError("end_date debe ser el último día del mismo mes")
        return self


class BudgetCreate(BudgetData):
    pass


class BudgetUpdate(BudgetData):
    pass


class BudgetOut(BudgetData):
    id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)


class BudgetProgress(BaseModel):
    budget_id: uuid.UUID
    category_id: uuid.UUID
    amount_limit: Decimal
    start_date: date
    end_date: date
    spent: Decimal
    percentage: Decimal
    status: BudgetStatus