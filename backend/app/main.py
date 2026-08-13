from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.v1.membership_packages import router as membership_packages_router
from app.db.session import get_db


app = FastAPI(
    title="Gym Management System",
    description="Gym administration and management API",
    version="1.0.0",
)


app.include_router(
    membership_packages_router,
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