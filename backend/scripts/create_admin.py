from sqlalchemy import select

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.role import Role
from app.models.user import User


def create_admin():
    db = SessionLocal()

    try:
        role = db.scalar(
            select(Role).where(Role.name == "admin")
        )

        if not role:
            role = Role(name="admin")
            db.add(role)
            db.flush()

        existing_user = db.scalar(
            select(User).where(
                User.email == "admin@gym.com"
            )
        )

        if existing_user:
            print("Admin user already exists.")
            return

        admin = User(
            username="admin",
            email="admin@gym.com",
            password_hash=hash_password("Admin@123"),
            full_name="Gym Administrator",
            is_active=True,
            role_id=role.id,
        )

        db.add(admin)
        db.commit()

        print("Admin user created successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    create_admin()