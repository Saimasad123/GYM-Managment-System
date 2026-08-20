from calendar import monthrange
from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.member import Member
from app.models.membership import Membership
from app.models.membership_package import MembershipPackage
from app.schemas.dashboard import ExpiringMembershipSummary
from app.schemas.membership import (
    MembershipCreate,
    MembershipResponse,
    MembershipStatusResponse,
    MembershipUpdate,
)


router = APIRouter(
    prefix="/memberships",
    tags=["Memberships"],
)


def add_months(start_date: date, months: int) -> date:
    month = start_date.month - 1 + months
    year = start_date.year + month // 12
    month = month % 12 + 1

    day = min(
        start_date.day,
        monthrange(year, month)[1],
    )

    return date(year, month, day)


@router.post(
    "",
    response_model=MembershipResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_membership(
    membership_data: MembershipCreate,
    db: Session = Depends(get_db),
):
    member = db.get(Member, membership_data.member_id)

    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found.",
        )

    package = db.get(
        MembershipPackage,
        membership_data.package_id,
    )

    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Membership package not found.",
        )

    if not package.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Membership package is inactive.",
        )

    expiry_date = add_months(
        membership_data.start_date,
        package.duration_months,
    )

    if membership_data.amount_paid > package.price:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Amount paid cannot exceed the package price.",
        )

    membership = Membership(
        member_id=membership_data.member_id,
        package_id=membership_data.package_id,
        start_date=membership_data.start_date,
        expiry_date=expiry_date,
        total_fee=package.price,
        amount_paid=membership_data.amount_paid,
        status="active",
    )

    db.add(membership)
    db.commit()
    db.refresh(membership)

    return membership


@router.get(
    "",
    response_model=list[MembershipResponse],
)
def get_memberships(
    db: Session = Depends(get_db),
):
    memberships = db.scalars(
        select(Membership)
        .order_by(Membership.id)
    ).all()

    return memberships


@router.get(
    "/active",
    response_model=list[MembershipResponse],
)
def get_active_memberships(
    db: Session = Depends(get_db),
):
    memberships = db.scalars(
        select(Membership)
        .where(Membership.status == "active")
        .order_by(Membership.id)
    ).all()

    return memberships


@router.get(
    "/expiring-soon",
    response_model=list[ExpiringMembershipSummary],
)
def get_expiring_soon_memberships(
    db: Session = Depends(get_db),
):
    today = date.today()
    expiring_threshold = today + timedelta(days=7)

    rows = db.execute(
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

    return [
        ExpiringMembershipSummary(
            id=row.id,
            member_id=row.member_id,
            member_name=row.full_name,
            expiry_date=row.expiry_date,
            end_date=row.expiry_date,
        )
        for row in rows
    ]


@router.get(
    "/expired",
    response_model=list[ExpiringMembershipSummary],
)
def get_expired_memberships(
    db: Session = Depends(get_db),
):
    today = date.today()

    rows = db.execute(
        select(
            Membership.id,
            Membership.member_id,
            Membership.expiry_date,
            Member.full_name,
        )
        .join(Member, Membership.member_id == Member.id)
        .where(
            Membership.expiry_date < today,
        )
        .order_by(Membership.expiry_date)
    ).all()

    return [
        ExpiringMembershipSummary(
            id=row.id,
            member_id=row.member_id,
            member_name=row.full_name,
            expiry_date=row.expiry_date,
            end_date=row.expiry_date,
        )
        for row in rows
    ]


@router.get(
    "/status",
    response_model=list[MembershipStatusResponse],
)
def get_all_membership_status(
    db: Session = Depends(get_db),
):
    today = date.today()

    rows = db.execute(
        select(
            Membership.id,
            Membership.member_id,
            Membership.start_date,
            Membership.expiry_date,
            Membership.total_fee,
            Membership.amount_paid,
            Membership.status,
            Member.full_name,
            Member.member_code,
            MembershipPackage.name,
            MembershipPackage.duration_months,
        )
        .join(Member, Membership.member_id == Member.id)
        .join(
            MembershipPackage,
            Membership.package_id == MembershipPackage.id,
        )
        .order_by(Membership.expiry_date)
    ).all()

    result = []

    for row in rows:
        balance = row.total_fee - row.amount_paid

        if balance <= 0:
            payment_status = "Paid"
        elif row.amount_paid > 0:
            payment_status = "Partial"
        else:
            payment_status = "Unpaid"

        if row.expiry_date < today:
            membership_status = "Expired"
        elif row.expiry_date <= today + timedelta(days=7):
            membership_status = "Expiring Soon"
        else:
            membership_status = "Active"

        days_remaining = (row.expiry_date - today).days

        result.append(
            MembershipStatusResponse(
                id=row.id,
                member_id=row.member_id,
                member_name=row.full_name,
                member_code=row.member_code,
                package_name=row.name,
                duration_months=row.duration_months,
                start_date=row.start_date,
                expiry_date=row.expiry_date,
                total_fee=row.total_fee,
                amount_paid=row.amount_paid,
                balance=balance,
                payment_status=payment_status,
                membership_status=membership_status,
                days_remaining=days_remaining
                if membership_status
                != "Expired"
                else 0,
            )
        )

    return result


@router.get(
    "/{membership_id}",
    response_model=MembershipResponse,
)
def get_membership(
    membership_id: int,
    db: Session = Depends(get_db),
):
    membership = db.get(
        Membership,
        membership_id,
    )

    if not membership:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Membership not found.",
        )

    return membership


@router.patch(
    "/{membership_id}",
    response_model=MembershipResponse,
)
def update_membership(
    membership_id: int,
    membership_data: MembershipUpdate,
    db: Session = Depends(get_db),
):
    membership = db.get(
        Membership,
        membership_id,
    )

    if not membership:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Membership not found.",
        )

    update_data = membership_data.model_dump(
        exclude_unset=True
    )

    if "amount_paid" in update_data:
        if update_data["amount_paid"] > membership.total_fee:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Amount paid cannot exceed the total fee.",
            )

    for field, value in update_data.items():
        setattr(membership, field, value)

    db.commit()
    db.refresh(membership)

    return membership


@router.post(
    "/{membership_id}/renew",
    response_model=MembershipResponse,
)
def renew_membership(
    membership_id: int,
    db: Session = Depends(get_db),
):
    membership = db.get(
        Membership,
        membership_id,
    )

    if not membership:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Membership not found.",
        )

    package = db.get(
        MembershipPackage,
        membership.package_id,
    )

    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Membership package not found.",
        )

    new_start_date = membership.expiry_date

    membership.start_date = new_start_date
    membership.expiry_date = add_months(
        new_start_date,
        package.duration_months,
    )
    membership.total_fee = package.price
    membership.amount_paid = 0
    membership.status = "active"

    db.commit()
    db.refresh(membership)

    return membership
