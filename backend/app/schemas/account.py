import uuid
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class AccountCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    type: Literal["cash", "bank", "savings", "credit_card"]
    currency: str = Field(default="COP", min_length=3, max_length=3)
    initial_balance: Decimal = Field(default=Decimal("0"))


class AccountOut(BaseModel):
    id: uuid.UUID
    name: str
    type: str
    currency: str
    current_balance: Decimal

    model_config = ConfigDict(from_attributes=True)