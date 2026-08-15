from decimal import Decimal

from pydantic import BaseModel


class DashboardSummary(BaseModel):
    total_members: int
    active_members: int
    expired_memberships: int
    today_revenue: Decimal
    monthly_revenue: Decimal
    total_memberships: int
