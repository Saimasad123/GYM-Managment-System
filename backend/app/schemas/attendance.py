from datetime import date, datetime, time

from pydantic import BaseModel, ConfigDict, Field


class AttendanceCreate(BaseModel):
    member_id: int = Field(gt=0)
    attendance_date: date | None = None
    check_in: time | None = None
    status: str = Field(default="present", max_length=20)


class AttendanceUpdate(BaseModel):
    check_in: time | None = None
    check_out: time | None = None
    status: str | None = Field(default=None, max_length=20)


class AttendanceResponse(BaseModel):
    id: int
    member_id: int
    attendance_date: date
    check_in: time | None
    check_out: time | None
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
