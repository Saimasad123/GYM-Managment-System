from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class TrainerCreate(BaseModel):
    trainer_code: str = Field(min_length=2, max_length=30)
    full_name: str = Field(min_length=2, max_length=150)
    phone: str = Field(min_length=7, max_length=30)
    specialization: str | None = Field(default=None, max_length=150)
    salary: Decimal = Field(default=0, ge=0)
    joining_date: date | None = None


class TrainerUpdate(BaseModel):
    trainer_code: str | None = Field(
        default=None,
        min_length=2,
        max_length=30,
    )
    full_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=150,
    )
    phone: str | None = Field(
        default=None,
        min_length=7,
        max_length=30,
    )
    specialization: str | None = Field(
        default=None,
        max_length=150,
    )
    salary: Decimal | None = Field(
        default=None,
        ge=0,
    )
    joining_date: date | None = None
    is_active: bool | None = None


class TrainerResponse(BaseModel):
    id: int
    trainer_code: str
    full_name: str
    phone: str
    specialization: str | None
    salary: Decimal
    joining_date: date
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)