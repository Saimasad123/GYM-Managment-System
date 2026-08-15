from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.attendance import Attendance
from app.models.member import Member
from app.schemas.attendance import (
    AttendanceCreate,
    AttendanceResponse,
    AttendanceUpdate,
)


router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"],
)


@router.post(
    "",
    response_model=AttendanceResponse,
    status_code=201,
)
def create_attendance(
    payload: AttendanceCreate,
    db: Session = Depends(get_db),
):
    member = db.scalar(
        select(Member).where(Member.id == payload.member_id)
    )

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Member not found",
        )

    attendance_date = payload.attendance_date or date.today()

    existing = db.scalar(
        select(Attendance).where(
            Attendance.member_id == payload.member_id,
            Attendance.attendance_date == attendance_date,
        )
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Attendance already exists for this member on this date",
        )

    attendance = Attendance(
        member_id=payload.member_id,
        attendance_date=attendance_date,
        check_in=payload.check_in,
        status=payload.status,
    )

    db.add(attendance)
    db.commit()
    db.refresh(attendance)

    return attendance


@router.get(
    "",
    response_model=list[AttendanceResponse],
)
def get_attendance(
    db: Session = Depends(get_db),
):
    return db.scalars(
        select(Attendance).order_by(
            Attendance.attendance_date.desc(),
            Attendance.id.desc(),
        )
    ).all()


@router.get(
    "/today",
    response_model=list[AttendanceResponse],
)
def get_today_attendance(
    db: Session = Depends(get_db),
):
    today = date.today()

    return db.scalars(
        select(Attendance)
        .where(Attendance.attendance_date == today)
        .order_by(Attendance.id.desc())
    ).all()


@router.get(
    "/member/{member_id}",
    response_model=list[AttendanceResponse],
)
def get_member_attendance(
    member_id: int,
    db: Session = Depends(get_db),
):
    member = db.scalar(
        select(Member).where(Member.id == member_id)
    )

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Member not found",
        )

    return db.scalars(
        select(Attendance)
        .where(Attendance.member_id == member_id)
        .order_by(Attendance.attendance_date.desc())
    ).all()


@router.patch(
    "/{attendance_id}",
    response_model=AttendanceResponse,
)
def update_attendance(
    attendance_id: int,
    payload: AttendanceUpdate,
    db: Session = Depends(get_db),
):
    attendance = db.scalar(
        select(Attendance).where(Attendance.id == attendance_id)
    )

    if not attendance:
        raise HTTPException(
            status_code=404,
            detail="Attendance record not found",
        )

    update_data = payload.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(attendance, field, value)

    db.commit()
    db.refresh(attendance)

    return attendance
