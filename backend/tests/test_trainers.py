import uuid

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def unique_trainer_code(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


def unique_phone() -> str:
    return f"03{uuid.uuid4().int % 10_000_000_000:010d}"


def test_create_trainer():
    trainer_code = unique_trainer_code("TR-TEST")

    response = client.post(
        "/api/v1/trainers",
        json={
            "trainer_code": trainer_code,
            "full_name": "Test Trainer",
            "phone": unique_phone(),
            "specialization": "Strength Training",
            "salary": 50000,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["trainer_code"] == trainer_code
    assert data["full_name"] == "Test Trainer"
    assert float(data["salary"]) == 50000
    assert data["is_active"] is True


def test_get_trainers():
    response = client.get(
        "/api/v1/trainers"
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_active_trainers():
    response = client.get(
        "/api/v1/trainers/active"
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_nonexistent_trainer():
    response = client.get(
        "/api/v1/trainers/999999"
    )

    assert response.status_code == 404


def test_duplicate_trainer_code():
    trainer_code = unique_trainer_code("TR-DUPLICATE")

    payload = {
        "trainer_code": trainer_code,
        "full_name": "Duplicate Trainer",
        "phone": unique_phone(),
        "salary": 40000,
    }

    first_response = client.post(
        "/api/v1/trainers",
        json=payload,
    )

    assert first_response.status_code == 201

    duplicate_response = client.post(
        "/api/v1/trainers",
        json={
            **payload,
            "phone": unique_phone(),
        },
    )

    assert duplicate_response.status_code == 409


def test_update_trainer():
    trainer_code = unique_trainer_code("TR-UPDATE")

    response = client.post(
        "/api/v1/trainers",
        json={
            "trainer_code": trainer_code,
            "full_name": "Before Update",
            "phone": unique_phone(),
            "salary": 45000,
        },
    )

    assert response.status_code == 201

    trainer_id = response.json()["id"]

    update_response = client.patch(
        f"/api/v1/trainers/{trainer_id}",
        json={
            "full_name": "After Update",
            "phone": unique_phone(),
        },
    )

    assert update_response.status_code == 200

    data = update_response.json()

    assert data["full_name"] == "After Update"


def test_deactivate_trainer():
    trainer_code = unique_trainer_code("TR-DEACTIVATE")

    response = client.post(
        "/api/v1/trainers",
        json={
            "trainer_code": trainer_code,
            "full_name": "Deactivate Trainer",
            "phone": unique_phone(),
            "salary": 40000,
        },
    )

    assert response.status_code == 201

    trainer_id = response.json()["id"]

    delete_response = client.delete(
        f"/api/v1/trainers/{trainer_id}"
    )

    assert delete_response.status_code == 200
    assert delete_response.json()["is_active"] is False