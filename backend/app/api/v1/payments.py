from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.member import Member
from app.models.membership import Membership
from app.models.payment import Payment
from app.schemas.payment import PaymentCreate, PaymentResponse


router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)


@router.post(
    "",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_payment(
    payment_data: PaymentCreate,
    db: Session = Depends(get_db),
):
    member = db.get(Member, payment_data.member_id)

    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found.",
        )

    membership = None

    if payment_data.membership_id is not None:
        membership = db.get(
            Membership,
            payment_data.membership_id,
        )

        if not membership:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Membership not found.",
            )

        if membership.member_id != payment_data.member_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Membership does not belong to this member.",
            )

    payment = Payment(
        member_id=payment_data.member_id,
        membership_id=payment_data.membership_id,
        amount=payment_data.amount,
        payment_method=payment_data.payment_method,
        reference_number=payment_data.reference_number,
        notes=payment_data.notes,
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return payment


@router.get(
    "",
    response_model=list[PaymentResponse],
)
def get_payments(
    year: int | None = Query(None),
    month: int | None = Query(None, ge=1, le=12),
    db: Session = Depends(get_db),
):
    query = select(Payment).order_by(Payment.payment_date.desc())

    if year is not None:
        query = query.where(
            func.extract("year", Payment.payment_date) == year
        )

    if month is not None:
        query = query.where(
            func.extract("month", Payment.payment_date) == month
        )

    return db.scalars(query).all()


@router.get(
    "/member/{member_id}",
    response_model=list[PaymentResponse],
)
def get_member_payments(
    member_id: int,
    db: Session = Depends(get_db),
):
    member = db.get(Member, member_id)

    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found.",
        )

    payments = db.scalars(
        select(Payment)
        .where(Payment.member_id == member_id)
        .order_by(Payment.payment_date.desc())
    ).all()

    return payments


@router.get(
    "/{payment_id}",
    response_model=PaymentResponse,
)
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db),
):
    payment = db.get(Payment, payment_id)

    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found.",
        )

    return payment