from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.staff import Staff
from app.schemas.staff import StaffCreate, StaffResponse, StaffUpdate


router = APIRouter(
    prefix="/staff",
    tags=["Staff"],
)


@router.post(
    "",
    response_model=StaffResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_staff(
    staff_data: StaffCreate,
    db: Session = Depends(get_db),
):
    existing = db.scalar(
        select(Staff).where(Staff.staff_code == staff_data.staff_code)
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Staff code already exists.",
        )

    staff = Staff(**staff_data.model_dump())
    db.add(staff)
    db.commit()
    db.refresh(staff)
    return staff


@router.get(
    "",
    response_model=list[StaffResponse],
)
def get_staff(
    db: Session = Depends(get_db),
):
    staff = db.scalars(
        select(Staff).order_by(Staff.id)
    ).all()
    return staff


@router.get(
    "/active",
    response_model=list[StaffResponse],
)
def get_active_staff(
    db: Session = Depends(get_db),
):
    staff = db.scalars(
        select(Staff)
        .where(Staff.is_active.is_(True))
        .order_by(Staff.id)
    ).all()
    return staff


@router.get(
    "/{staff_id}",
    response_model=StaffResponse,
)
def get_staff_member(
    staff_id: int,
    db: Session = Depends(get_db),
):
    staff = db.get(Staff, staff_id)
    if not staff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Staff not found.",
        )
    return staff


@router.patch(
    "/{staff_id}",
    response_model=StaffResponse,
)
def update_staff(
    staff_id: int,
    staff_data: StaffUpdate,
    db: Session = Depends(get_db),
):
    staff = db.get(Staff, staff_id)
    if not staff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Staff not found.",
        )

    if staff_data.staff_code and staff_data.staff_code != staff.staff_code:
        existing = db.scalar(
            select(Staff).where(Staff.staff_code == staff_data.staff_code)
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Staff code already exists.",
            )

    update_data = staff_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(staff, field, value)

    db.commit()
    db.refresh(staff)
    return staff


@router.delete(
    "/{staff_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def deactivate_staff(
    staff_id: int,
    db: Session = Depends(get_db),
):
    staff = db.get(Staff, staff_id)
    if not staff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Staff not found.",
        )

    staff.is_active = False
    db.commit()
