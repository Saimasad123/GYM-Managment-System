from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.api.v1.members import router as members_router
from app.api.v1.auth import router as auth_router
from app.api.v1.memberships import router as memberships_router
from app.api.v1.payments import router as payments_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.trainers import router as trainers_router
from app.api.v1.attendance import router as attendance_router
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.expenses import router as expenses_router
from app.api.v1.membership_packages import (
    router as membership_packages_router,
)
from app.api.v1.staff import router as staff_router
from app.api.v1.reminders import router as reminders_router
from app.db.session import Base, engine, get_db, warmup_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    warmup_connection()
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Gym Management System",
    description="Gym administration and management API",
    version="1.0.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    auth_router,
    prefix="/api/v1",
)
app.include_router(
    members_router,
    prefix="/api/v1",
)

app.include_router(
    membership_packages_router,
    prefix="/api/v1",
)

app.include_router(
    payments_router,
    prefix="/api/v1",
)

app.include_router(
    memberships_router,
    prefix="/api/v1",
)

app.include_router(
    dashboard_router,
    prefix="/api/v1",
)
app.include_router(
    attendance_router,
    prefix="/api/v1",
)
app.include_router(
    trainers_router,
    prefix="/api/v1",
)

app.include_router(
    expenses_router,
    prefix="/api/v1",
)

app.include_router(
    staff_router,
    prefix="/api/v1",
)

app.include_router(
    reminders_router,
    prefix="/api/v1",
)


@app.get("/")
def root():
    return {
        "message": "Gym Management System API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.get("/health/database")
def database_health(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1"))

    return {
        "database": "connected",
        "result": result.scalar(),
    }