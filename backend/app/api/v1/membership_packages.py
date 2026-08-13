from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.membership_package import MembershipPackage
from app.schemas.membership_package import (
    MembershipPackageCreate,
    MembershipPackageResponse,
    MembershipPackageUpdate,
)


router = APIRouter(
    prefix="/membership-packages",
    tags=["Membership Packages"],
)


@router.post(
    "",
    response_model=MembershipPackageResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_package(
    package_data: MembershipPackageCreate,
    db: Session = Depends(get_db),
):
    existing_package = db.scalar(
        select(MembershipPackage).where(
            MembershipPackage.name == package_data.name
        )
    )

    if existing_package:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A package with this name already exists.",
        )

    package = MembershipPackage(
        name=package_data.name,
        duration_months=package_data.duration_months,
        price=package_data.price,
        description=package_data.description,
    )

    db.add(package)
    db.commit()
    db.refresh(package)

    return package


@router.get(
    "",
    response_model=list[MembershipPackageResponse],
)
def get_packages(
    db: Session = Depends(get_db),
):
    packages = db.scalars(
        select(MembershipPackage)
        .order_by(MembershipPackage.id)
    ).all()

    return packages


@router.get(
    "/active",
    response_model=list[MembershipPackageResponse],
)
def get_active_packages(
    db: Session = Depends(get_db),
):
    packages = db.scalars(
        select(MembershipPackage)
        .where(MembershipPackage.is_active.is_(True))
        .order_by(MembershipPackage.id)
    ).all()

    return packages


@router.get(
    "/{package_id}",
    response_model=MembershipPackageResponse,
)
def get_package(
    package_id: int,
    db: Session = Depends(get_db),
):
    package = db.get(MembershipPackage, package_id)

    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Membership package not found.",
        )

    return package


@router.patch(
    "/{package_id}",
    response_model=MembershipPackageResponse,
)
def update_package(
    package_id: int,
    package_data: MembershipPackageUpdate,
    db: Session = Depends(get_db),
):
    package = db.get(MembershipPackage, package_id)

    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Membership package not found.",
        )

    update_data = package_data.model_dump(
        exclude_unset=True
    )

    if "name" in update_data:
        existing_package = db.scalar(
            select(MembershipPackage).where(
                MembershipPackage.name == update_data["name"],
                MembershipPackage.id != package_id,
            )
        )

        if existing_package:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A package with this name already exists.",
            )

    for field, value in update_data.items():
        setattr(package, field, value)

    db.commit()
    db.refresh(package)

    return package


@router.delete(
    "/{package_id}",
    response_model=MembershipPackageResponse,
)
def deactivate_package(
    package_id: int,
    db: Session = Depends(get_db),
):
    package = db.get(MembershipPackage, package_id)

    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Membership package not found.",
        )

    package.is_active = False

    db.commit()
    db.refresh(package)

    return package
