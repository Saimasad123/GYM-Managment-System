from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Membership(Base):
    __tablename__ = "memberships"

    id: Mapped[int] = mapped_column(primary_key=True)

    member_id: Mapped[int] = mapped_column(
        ForeignKey("members.id"),
        nullable=False,
        index=True,
    )

    package_id: Mapped[int] = mapped_column(
        ForeignKey("membership_packages.id"),
        nullable=False,
    )

    start_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    expiry_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )

    total_fee: Mapped[float] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    amount_paid: Mapped[float] = mapped_column(
        Numeric(12, 2),
        default=0,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="active",
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    member = relationship(
        "Member",
        back_populates="memberships",
    )

    package = relationship(
        "MembershipPackage",
        back_populates="memberships",
    )

    payments = relationship(
        "Payment",
        back_populates="membership",
    )
