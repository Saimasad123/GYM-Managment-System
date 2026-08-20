from datetime import date, timedelta
from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.attendance import Attendance
from app.models.expense import Expense
from app.models.member import Member
from app.models.membership import Membership
from app.models.payment import Payment
from app.models.trainer import Trainer
from app.schemas.dashboard import (
    DashboardSummary,
    DailyFinancialSummary,
    ExpiringMembershipSummary,
)


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

    # Current month
    month_start = today.replace(day=1)

    # Current year
    year_start = today.replace(
        month=1,
        day=1,
    )

    # --------------------------------------------------
    # MEMBER STATISTICS
    # --------------------------------------------------

    total_members = db.scalar(
        select(func.count(Member.id))
    ) or 0

    active_members = db.scalar(
        select(func.count(Member.id)).where(
            Member.is_active.is_(True)
        )
    ) or 0

    expired_memberships = db.scalar(
        select(func.count(Membership.id)).where(
            Membership.expiry_date < today
        )
    ) or 0

    total_memberships = db.scalar(
        select(func.count(Membership.id))
    ) or 0

    total_trainers = db.scalar(
        select(func.count(Trainer.id))
    ) or 0

    today_attendance = db.scalar(
        select(func.count(Attendance.id)).where(
            Attendance.attendance_date == today
        )
    ) or 0

    # --------------------------------------------------
    # EXPIRING SOON MEMBERSHIPS
    # --------------------------------------------------

    expiring_threshold = today + timedelta(days=7)

    expiring_rows = db.execute(
        select(
            Membership.id,
            Membership.member_id,
            Membership.expiry_date,
            Member.full_name,
        )
        .join(Member, Membership.member_id == Member.id)
        .where(
            Membership.expiry_date >= today,
            Membership.expiry_date <= expiring_threshold,
        )
        .order_by(Membership.expiry_date)
    ).all()

    expiring_soon = [
        ExpiringMembershipSummary(
            id=row.id,
            member_id=row.member_id,
            member_name=row.full_name,
            expiry_date=row.expiry_date,
            end_date=row.expiry_date,
        )
        for row in expiring_rows
    ]

    # --------------------------------------------------
    # TODAY
    # --------------------------------------------------

    today_revenue = db.scalar(
        select(
            func.coalesce(
                func.sum(Payment.amount),
                0,
            )
        ).where(
            func.date(Payment.payment_date) == today
        )
    ) or Decimal("0")

    today_expenses = db.scalar(
        select(
            func.coalesce(
                func.sum(Expense.amount),
                0,
            )
        ).where(
            func.date(Expense.expense_date) == today
        )
    ) or Decimal("0")

    today_profit = (
        today_revenue - today_expenses
    )

    # --------------------------------------------------
    # CURRENT MONTH
    # --------------------------------------------------

    monthly_revenue = db.scalar(
        select(
            func.coalesce(
                func.sum(Payment.amount),
                0,
            )
        ).where(
            Payment.payment_date >= month_start
        )
    ) or Decimal("0")

    monthly_expenses = db.scalar(
        select(
            func.coalesce(
                func.sum(Expense.amount),
                0,
            )
        ).where(
            Expense.expense_date >= month_start
        )
    ) or Decimal("0")

    monthly_profit = (
        monthly_revenue - monthly_expenses
    )

    # --------------------------------------------------
    # CURRENT YEAR
    # --------------------------------------------------

    annual_revenue = db.scalar(
        select(
            func.coalesce(
                func.sum(Payment.amount),
                0,
            )
        ).where(
            Payment.payment_date >= year_start
        )
    ) or Decimal("0")

    annual_expenses = db.scalar(
        select(
            func.coalesce(
                func.sum(Expense.amount),
                0,
            )
        ).where(
            Expense.expense_date >= year_start
        )
    ) or Decimal("0")

    annual_profit = (
        annual_revenue - annual_expenses
    )

    # --------------------------------------------------
    # DAILY FINANCIAL REPORT
    # --------------------------------------------------

    revenue_by_date = db.execute(
        select(
            func.date(Payment.payment_date).label("date"),
            func.sum(Payment.amount).label("revenue"),
        )
        .where(
            Payment.payment_date >= year_start
        )
        .group_by(
            func.date(Payment.payment_date)
        )
    ).all()

    expense_by_date = db.execute(
        select(
            func.date(Expense.expense_date).label("date"),
            func.sum(Expense.amount).label("expenses"),
        )
        .where(
            Expense.expense_date >= year_start
        )
        .group_by(
            func.date(Expense.expense_date)
        )
    ).all()

    financial_by_date = {}

    for row in revenue_by_date:
        financial_by_date[row.date] = {
            "revenue": row.revenue or Decimal("0"),
            "expenses": Decimal("0"),
        }

    for row in expense_by_date:
        if row.date not in financial_by_date:
            financial_by_date[row.date] = {
                "revenue": Decimal("0"),
                "expenses": Decimal("0"),
            }

        financial_by_date[row.date]["expenses"] = (
            row.expenses or Decimal("0")
        )

    daily_financials = []

    for financial_date in sorted(
        financial_by_date.keys(),
        reverse=True,
    ):
        revenue = financial_by_date[
            financial_date
        ]["revenue"]

        expenses = financial_by_date[
            financial_date
        ]["expenses"]

        daily_financials.append(
            DailyFinancialSummary(
                date=financial_date,
                revenue=revenue,
                expenses=expenses,
                profit=revenue - expenses,
            )
        )

    # --------------------------------------------------
    # RESPONSE
    # --------------------------------------------------

    return DashboardSummary(
        total_members=total_members,
        active_members=active_members,
        expired_memberships=expired_memberships,
        total_memberships=total_memberships,

        total_trainers=total_trainers,
        today_attendance=today_attendance,

        today_revenue=today_revenue,
        today_expenses=today_expenses,
        today_profit=today_profit,

        monthly_revenue=monthly_revenue,
        monthly_expenses=monthly_expenses,
        monthly_profit=monthly_profit,

        annual_revenue=annual_revenue,
        annual_expenses=annual_expenses,
        annual_profit=annual_profit,

        expiring_soon=expiring_soon,
        daily_financials=daily_financials,
    )