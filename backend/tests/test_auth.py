from fastapi.testclient import TestClient
from sqlalchemy import select

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.main import app
from app.models.role import Role
from app.models.user import User


client = TestClient(app)


def create_test_user():
    db = SessionLocal()

    try:
        role = db.scalar(
            select(Role).where(Role.name == "admin")
        )

        if not role:
            role = Role(name="admin")
            db.add(role)
            db.flush()

        user = db.scalar(
            select(User).where(
                User.email == "testadmin@gym.com"
            )
        )

        if not user:
            user = User(
                username="testadmin",
                email="testadmin@gym.com",
                password_hash=hash_password("Test@123"),
                full_name="Test Administrator",
                is_active=True,
                role_id=role.id,
            )

            db.add(user)
            db.commit()
            db.refresh(user)

        return user

    finally:
        db.close()


def test_login_success():
    create_test_user()

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "testadmin@gym.com",
            "password": "Test@123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password():
    create_test_user()

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "testadmin@gym.com",
            "password": "WrongPassword",
        },
    )

    assert response.status_code == 401


def test_login_nonexistent_user():
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "doesnotexist@gym.com",
            "password": "Test@123",
        },
    )

    assert response.status_code == 401



def test_me_without_token():
    response = client.get(
        "/api/v1/auth/me"
    )

    assert response.status_code == 401

def test_me_with_invalid_token():
    response = client.get(
        "/api/v1/auth/me",
        headers={
            "Authorization": "Bearer invalid-token"
        },
    )

    assert response.status_code == 401


def test_me_with_valid_token():
    create_test_user()

    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "testadmin@gym.com",
            "password": "Test@123",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.get(
        "/api/v1/auth/me",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == "testadmin@gym.com"
    assert data["username"] == "testadmin"
    assert data["is_active"] is True