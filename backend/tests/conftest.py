from sqlalchemy import create_engine

from app.core.config import settings
from app.db.session import Base, engine


def pytest_configure(config):
    from app.models.attendance import Attendance
    from app.models.expense import Expense
    from app.models.member import Member
    from app.models.membership import Membership
    from app.models.membership_package import MembershipPackage
    from app.models.payment import Payment
    from app.models.reminder import Reminder
    from app.models.role import Role
    from app.models.staff import Staff
    from app.models.trainer import Trainer
    from app.models.user import User

    Base.metadata.create_all(bind=engine)
