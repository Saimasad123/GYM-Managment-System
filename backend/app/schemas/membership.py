from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class MembershipCreate(BaseModel):
    member_id: int = Field(gt=0)
    package_id: int = Field(gt=0)
    start_date: date
    amount_paid: Decimal = Field(default=Decimal("0.00"), ge=0)


class MembershipUpdate(BaseModel):
    amount_paid: Decimal | None = Field(default=None, ge=0)
    status: str | None = Field(default=None, max_length=20)


class MembershipResponse(BaseModel):
    id: int
    member_id: int
    package_id: int
    start_date: date
    expiry_date: date
    total_fee: Decimal
    amount_paid: Decimal
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
