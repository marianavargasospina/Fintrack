import uuid
from datetime import date
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


TransactionType = Literal["income", "expense", "transfer"]


class TransactionData(BaseModel):
    account_id: uuid.UUID
    category_id: uuid.UUID | None = None
    type: TransactionType
    amount: Decimal = Field(gt=0)
    description: str | None = Field(default=None, max_length=255)
    transaction_date: date
    destination_account_id: uuid.UUID | None = None

    @model_validator(mode="after")
    def validate_transaction_fields(self):
        if self.type == "transfer":
            if self.category_id is not None:
                raise ValueError("Las transferencias no pueden tener categoría")
            if self.destination_account_id is None:
                raise ValueError("Las transferencias requieren una cuenta destino")
            if self.account_id == self.destination_account_id:
                raise ValueError("La cuenta origen y destino deben ser diferentes")
        elif self.category_id is None:
            raise ValueError("Los ingresos y gastos requieren una categoría")
        elif self.destination_account_id is not None:
            raise ValueError(
                "Los ingresos y gastos no pueden tener cuenta destino"
            )
        return self


class TransactionCreate(TransactionData):
    pass


class TransactionUpdate(TransactionData):
    pass


class TransactionOut(TransactionData):
    id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)


class TransactionPage(BaseModel):
    items: list[TransactionOut]
    total: int
    page: int
    page_size: int
    pages: int