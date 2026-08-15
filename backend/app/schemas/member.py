from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class MemberBase(BaseModel):
    full_name: str = Field(min_length=2, max_length=150)
    father_name: str | None = Field(default=None, max_length=150)
    phone: str = Field(min_length=3, max_length=30)
    cnic: str | None = Field(default=None, max_length=30)
    date_of_birth: date | None = None
    gender: str | None = Field(default=None, max_length=20)
    address: str | None = Field(default=None, max_length=500)
    emergency_contact: str | None = Field(default=None, max_length=30)


class MemberCreate(MemberBase):
    member_code: str = Field(min_length=1, max_length=30)


class MemberUpdate(BaseModel):
    member_code: str | None = Field(default=None, min_length=1, max_length=30)
    full_name: str | None = Field(default=None, min_length=2, max_length=150)
    father_name: str | None = Field(default=None, max_length=150)
    phone: str | None = Field(default=None, min_length=3, max_length=30)
    cnic: str | None = Field(default=None, max_length=30)
    date_of_birth: date | None = None
    gender: str | None = Field(default=None, max_length=20)
    address: str | None = Field(default=None, max_length=500)
    emergency_contact: str | None = Field(default=None, max_length=30)
    is_active: bool | None = None


class MemberResponse(MemberBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    member_code: str
    joining_date: date
    is_active: bool
    created_at: datetime