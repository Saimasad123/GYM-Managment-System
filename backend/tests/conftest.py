from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings
from app.db.session import Base


def pytest_configure(config):
    engine = create_engine(settings.DATABASE_URL)
    Base.metadata.create_all(bind=engine)
