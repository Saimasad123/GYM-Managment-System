from calendar import monthrange
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.member import Member
from app.models.membership import Membership
from app.models.membership_package import MembershipPackage
from app.schemas.membership import (
    MembershipCreate,
    MembershipResponse,
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
