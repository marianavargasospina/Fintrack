import uuid
from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class SavingsGoalCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    target_amount: Decimal = Field(gt=0)
    current_amount: Decimal = Field(default=Decimal("0"), ge=0)
    target_date: date


class SavingsGoalProgress(BaseModel):
    current_amount: Decimal = Field(ge=0)


class SavingsGoalOut(SavingsGoalCreate):
    id: uuid.UUID
    percentage: Decimal

    model_config = ConfigDict(from_attributes=True)