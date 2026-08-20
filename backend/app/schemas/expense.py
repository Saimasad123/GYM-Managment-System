from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ExpenseCreate(BaseModel):
    category: str = Field(min_length=2, max_length=50)
    description: str = Field(min_length=2, max_length=500)
    amount: Decimal = Field(gt=0)
    payment_method: str = Field(min_length=2, max_length=30)
    reference_number: str | None = Field(
        default=None,
        max_length=100,
    )
    notes: str | None = Field(
        default=None,
        max_length=500,
    )


class ExpenseUpdate(BaseModel):
    category: str | None = Field(
        default=None,
        min_length=2,
        max_length=50,
    )
    description: str | None = Field(
        default=None,
        min_length=2,
        max_length=500,
    )
    amount: Decimal | None = Field(
        default=None,
        gt=0,
    )
    payment_method: str | None = Field(
        default=None,
        min_length=2,
        max_length=30,
    )
    reference_number: str | None = Field(
        default=None,
        max_length=100,
    )
    notes: str | None = Field(
        default=None,
        max_length=500,
    )


class ExpenseResponse(BaseModel):
    id: int
    category: str
    description: str
    amount: Decimal
    payment_method: str
    reference_number: str | None
    notes: str | None
    expense_date: datetime

    model_config = ConfigDict(from_attributes=True)
