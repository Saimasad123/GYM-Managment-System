from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.trainer import Trainer
from app.schemas.trainer import (
    TrainerCreate,
    TrainerResponse,
    TrainerUpdate,
)


router = APIRouter(
    prefix="/trainers",
    tags=["Trainers"],
)


@router.post(
    "",
    response_model=TrainerResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_trainer(
    trainer_data: TrainerCreate,
    db: Session = Depends(get_db),
):
    existing_trainer = db.scalar(
        select(Trainer).where(
            Trainer.trainer_code == trainer_data.trainer_code
        )
    )

    if existing_trainer:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A trainer with this code already exists.",
        )

    trainer = Trainer(
        trainer_code=trainer_data.trainer_code,
        full_name=trainer_data.full_name,
        phone=trainer_data.phone,
        specialization=trainer_data.specialization,
        salary=trainer_data.salary,
        joining_date=trainer_data.joining_date,
    )

    db.add(trainer)
    db.commit()
    db.refresh(trainer)

    return trainer


@router.get(
    "",
    response_model=list[TrainerResponse],
)
def get_trainers(
    db: Session = Depends(get_db),
):
    trainers = db.scalars(
        select(Trainer).order_by(Trainer.id)
    ).all()

    return trainers


@router.get(
    "/active",
    response_model=list[TrainerResponse],
)
def get_active_trainers(
    db: Session = Depends(get_db),
):
    trainers = db.scalars(
        select(Trainer)
        .where(Trainer.is_active.is_(True))
        .order_by(Trainer.id)
    ).all()

    return trainers


@router.get(
    "/{trainer_id}",
    response_model=TrainerResponse,
)
def get_trainer(
    trainer_id: int,
    db: Session = Depends(get_db),
):
    trainer = db.get(Trainer, trainer_id)

    if not trainer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trainer not found.",
        )

    return trainer


@router.patch(
    "/{trainer_id}",
    response_model=TrainerResponse,
)
def update_trainer(
    trainer_id: int,
    trainer_data: TrainerUpdate,
    db: Session = Depends(get_db),
):
    trainer = db.get(Trainer, trainer_id)

    if not trainer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trainer not found.",
        )

    update_data = trainer_data.model_dump(
        exclude_unset=True
    )

    if "trainer_code" in update_data:
        existing_trainer = db.scalar(
            select(Trainer).where(
                Trainer.trainer_code == update_data["trainer_code"],
                Trainer.id != trainer_id,
            )
        )

        if existing_trainer:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A trainer with this code already exists.",
            )

    for field, value in update_data.items():
        setattr(trainer, field, value)

    db.commit()
    db.refresh(trainer)

    return trainer


@router.delete(
    "/{trainer_id}",
    response_model=TrainerResponse,
)
def deactivate_trainer(
    trainer_id: int,
    db: Session = Depends(get_db),
):
    trainer = db.get(Trainer, trainer_id)

    if not trainer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trainer not found.",
        )

    trainer.is_active = False

    db.commit()
    db.refresh(trainer)

    return trainer