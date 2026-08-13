from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class MembershipPackageCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    duration_months: int = Field(gt=0)
    price: float = Field(ge=0)
    description: str | None = Field(default=None, max_length=500)


class MembershipPackageUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    duration_months: int | None = Field(default=None, gt=0)
    price: float | None = Field(default=None, ge=0)
    description: str | None = Field(default=None, max_length=500)
    is_active: bool | None = None


class MembershipPackageResponse(BaseModel):
    id: int
    name: str
    duration_months: int
    price: float
    description: str | None
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

