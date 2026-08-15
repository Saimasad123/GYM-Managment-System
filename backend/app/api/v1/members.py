from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.member import Member
from app.schemas.member import (
    MemberCreate,
    MemberResponse,
    MemberUpdate,
)


router = APIRouter(
    prefix="/members",
    tags=["Members"],
)


@router.post(
    "",
    response_model=MemberResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_member(
    member_data: MemberCreate,
    db: Session = Depends(get_db),
):
    existing_member = db.scalar(
        select(Member).where(
            or_(
                Member.member_code == member_data.member_code,
                Member.cnic == member_data.cnic
                if member_data.cnic
                else False,
            )
        )
    )

    if existing_member:
        if existing_member.member_code == member_data.member_code:
            detail = "A member with this member code already exists."
        else:
            detail = "A member with this CNIC already exists."

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
        )

    member = Member(
        **member_data.model_dump(),
    )

    db.add(member)
    db.commit()
    db.refresh(member)

    return member


@router.get(
    "",
    response_model=list[MemberResponse],
)
def get_members(
    db: Session = Depends(get_db),
):
    members = db.scalars(
        select(Member)
        .order_by(Member.id)
    ).all()

    return members


@router.get(
    "/active",
    response_model=list[MemberResponse],
)
def get_active_members(
    db: Session = Depends(get_db),
):
    members = db.scalars(
        select(Member)
        .where(Member.is_active.is_(True))
        .order_by(Member.id)
    ).all()

    return members


@router.get(
    "/{member_id}",
    response_model=MemberResponse,
)
def get_member(
    member_id: int,
    db: Session = Depends(get_db),
):
    member = db.get(Member, member_id)

    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found.",
        )

    return member


@router.patch(
    "/{member_id}",
    response_model=MemberResponse,
)
def update_member(
    member_id: int,
    member_data: MemberUpdate,
    db: Session = Depends(get_db),
):
    member = db.get(Member, member_id)

    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found.",
        )

    update_data = member_data.model_dump(
        exclude_unset=True
    )

    if "member_code" in update_data:
        existing_member = db.scalar(
            select(Member).where(
                Member.member_code == update_data["member_code"],
                Member.id != member_id,
            )
        )

        if existing_member:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A member with this member code already exists.",
            )

    if "cnic" in update_data and update_data["cnic"]:
        existing_member = db.scalar(
            select(Member).where(
                Member.cnic == update_data["cnic"],
                Member.id != member_id,
            )
        )

        if existing_member:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A member with this CNIC already exists.",
            )

    for field, value in update_data.items():
        setattr(member, field, value)

    db.commit()
    db.refresh(member)

    return member


@router.delete(
    "/{member_id}",
    response_model=MemberResponse,
)
def deactivate_member(
    member_id: int,
    db: Session = Depends(get_db),
):
    member = db.get(Member, member_id)

    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found.",
        )

    member.is_active = False

    db.commit()
    db.refresh(member)

    return member