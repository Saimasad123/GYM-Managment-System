from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class DailyFinancialSummary(BaseModel):
    date: date
    revenue: Decimal
    expenses: Decimal
    profit: Decimal


class ExpiringMembershipSummary(BaseModel):
    id: int
    member_id: int
    member_name: str | None = None
    expiry_date: date
    end_date: date | None = None

    model_config = ConfigDict(from_attributes=True)


class DashboardSummary(BaseModel):
    total_members: int
    active_members: int
    expired_memberships: int
    total_memberships: int

    total_trainers: int
    today_attendance: int

    today_revenue: Decimal
    today_expenses: Decimal
    today_profit: Decimal

    monthly_revenue: Decimal
    monthly_expenses: Decimal
    monthly_profit: Decimal

    annual_revenue: Decimal
    annual_expenses: Decimal
    annual_profit: Decimal

    expiring_soon: list[ExpiringMembershipSummary]
    daily_financials: list[DailyFinancialSummary]