import uuid
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


CategoryType = Literal["income", "expense"]


class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    type: CategoryType


class CategoryUpdate(CategoryCreate):
    pass


class CategoryOut(BaseModel):
    id: uuid.UUID
    name: str
    type: CategoryType

    model_config = ConfigDict(from_attributes=True)