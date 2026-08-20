from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.member import Member
from app.models.membership import Membership
from app.models.membership_package import MembershipPackage
from app.models.reminder import Reminder
from app.schemas.reminder import (
    MembershipReminderResponse,
    ReminderCreate,
    ReminderResponse,
)


router = APIRouter(
    prefix="/reminders",
    tags=["Reminders"],
)


def get_upcoming_expirations(db: Session, days: int = 2):
    today = date.today()
    threshold = today + timedelta(days=days)

    rows = db.execute(
        select(
            Membership.id,
            Membership.member_id,
            Membership.expiry_date,
            Member.full_name,
            Member.member_code,
            MembershipPackage.name,
        )
        .join(Member, Membership.member_id == Member.id)
        .join(
            MembershipPackage,
            Membership.package_id == MembershipPackage.id,
        )
        .where(
            Membership.expiry_date >= today,
            Membership.expiry_date <= threshold,
        )
        .order_by(Membership.expiry_date)
    ).all()

    result = []

    for row in rows:
        days_remaining = (row.expiry_date - today).days

        result.append(
            {
                "id": row.id,
                "member_id": row.member_id,
                "member_name": row.full_name,
                "member_code": row.member_code,
                "package_name": row.name,
                "expiry_date": row.expiry_date,
                "days_remaining": days_remaining,
                "reminder_type": "payment_due",
                "message": f"Membership expiring in {days_remaining} day(s). Please pay fees to renew.",
            }
        )

    return result


@router.get(
    "/upcoming",
    response_model=list[MembershipReminderResponse],
)
def get_upcoming_reminders(
    days: int = 2,
    db: Session = Depends(get_db),
):
    reminders = get_upcoming_expirations(db, days=days)
    return reminders


@router.post(
    "",
    response_model=ReminderResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_reminder(
    reminder_data: ReminderCreate,
    db: Session = Depends(get_db),
):
    membership = db.get(Membership, reminder_data.membership_id)

    if not membership:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Membership not found.",
        )

    reminder = Reminder(**reminder_data.model_dump())
    db.add(reminder)
    db.commit()
    db.refresh(reminder)

    return reminder


@router.get(
    "",
    response_model=list[ReminderResponse],
)
def get_reminders(
    is_sent: bool | None = None,
    db: Session = Depends(get_db),
):
    query = select(Reminder).order_by(Reminder.reminder_date.desc())

    if is_sent is not None:
        query = query.where(Reminder.is_sent == is_sent)

    reminders = db.scalars(query).all()
    return reminders


@router.patch(
    "/{reminder_id}/send",
    response_model=ReminderResponse,
)
def mark_reminder_sent(
    reminder_id: int,
    db: Session = Depends(get_db),
):
    reminder = db.get(Reminder, reminder_id)

    if not reminder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found.",
        )

    reminder.is_sent = True
    reminder.sent_at = date.today()

    db.commit()
    db.refresh(reminder)

    return reminder


@router.get(
    "/member/{member_id}",
    response_model=list[ReminderResponse],
)
def get_member_reminders(
    member_id: int,
    db: Session = Depends(get_db),
):
    member = db.get(Member, member_id)

    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found.",
        )

    reminders = db.scalars(
        select(Reminder)
        .join(Membership, Reminder.membership_id == Membership.id)
        .where(Membership.member_id == member_id)
        .order_by(Reminder.reminder_date.desc())
    ).all()

    return reminders
