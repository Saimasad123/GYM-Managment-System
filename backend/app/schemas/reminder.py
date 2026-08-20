from datetime import date, datetime
from pydantic import BaseModel, ConfigDict


class ReminderBase(BaseModel):
    membership_id: int
    reminder_date: date
    reminder_type: str
    message: str


class ReminderCreate(ReminderBase):
    pass


class ReminderResponse(ReminderBase):
    id: int
    is_sent: bool
    sent_at: datetime | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MembershipReminderResponse(BaseModel):
    id: int
    member_id: int
    member_name: str | None = None
    member_code: str | None = None
    package_name: str | None = None
    expiry_date: date
    days_remaining: int
    reminder_type: str
    message: str

    model_config = ConfigDict(from_attributes=True)
