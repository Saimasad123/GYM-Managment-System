from datetime import date, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.member import Member
from app.models.membership import Membership
from app.models.payment import Payment
from app.schemas.dashboard import DashboardSummary


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "/summary",
    response_model=DashboardSummary,
)
def get_dashboard_summary(
    db: Session = Depends(get_db),
):
    today = date.today()

    # First day of the current month
    month_start = today.replace(day=1)

    # Total members
    total_members = db.scalar(
        select(func.count(Member.id))
    ) or 0

    # Active members
    active_members = db.scalar(
        select(func.count(Member.id)).where(
            Member.is_active.is_(True)
        )
    ) or 0

    # Expired memberships
    expired_memberships = db.scalar(
        select(func.count(Membership.id)).where(
            Membership.expiry_date < today
        )
    ) or 0

    # Total memberships
    total_memberships = db.scalar(
        select(func.count(Membership.id))
    ) or 0

    # Today's revenue
    today_revenue = db.scalar(
        select(func.coalesce(func.sum(Payment.amount), 0)).where(
            func.date(Payment.payment_date) == today
        )
    ) or 0

    # Current month's revenue
    monthly_revenue = db.scalar(
        select(func.coalesce(func.sum(Payment.amount), 0)).where(
            Payment.payment_date >= month_start
        )
    ) or 0

    return DashboardSummary(
        total_members=total_members,
        active_members=active_members,
        expired_memberships=expired_memberships,
        today_revenue=today_revenue,
        monthly_revenue=monthly_revenue,
        total_memberships=total_memberships,
    )
