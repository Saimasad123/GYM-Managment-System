from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, Field


class StaffBase(BaseModel):
    staff_code: str
    full_name: str
    phone: str
    email: str | None = None
    role: str
    department: str | None = None
    salary: int | None = None
    joining_date: date | None = None


class StaffCreate(StaffBase):
    pass


class StaffUpdate(BaseModel):
    staff_code: str | None = None
    full_name: str | None = None
    phone: str | None = None
    email: str | None = None
    role: str | None = None
    department: str | None = None
    salary: int | None = None
    joining_date: date | None = None
    is_active: bool | None = None


class StaffResponse(StaffBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
