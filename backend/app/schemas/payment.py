from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class PaymentCreate(BaseModel):
    member_id: int = Field(gt=0)
    membership_id: int | None = Field(default=None, gt=0)
    amount: Decimal = Field(gt=0)
    payment_method: str = Field(min_length=2, max_length=30)
    reference_number: str | None = Field(default=None, max_length=100)
    notes: str | None = Field(default=None, max_length=500)


class PaymentResponse(BaseModel):
    id: int
    member_id: int
    membership_id: int | None
    amount: Decimal
    payment_method: str
    reference_number: str | None
    notes: str | None
    payment_date: datetime

    model_config = ConfigDict(from_attributes=True)
