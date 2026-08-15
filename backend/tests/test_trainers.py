from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_trainer():
    response = client.post(
        "/api/v1/trainers",
        json={
            "trainer_code": "TR-TEST-001",
            "full_name": "Test Trainer",
            "phone": "03005555555",
            "specialization": "Strength Training",
            "salary": 50000,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["trainer_code"] == "TR-TEST-001"
    assert data["full_name"] == "Test Trainer"
    assert data["is_active"] is True


def test_get_trainers():
    response = client.get("/api/v1/trainers")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_active_trainers():
    response = client.get("/api/v1/trainers/active")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_nonexistent_trainer():
    response = client.get("/api/v1/trainers/999999")

    assert response.status_code == 404


def test_duplicate_trainer_code():
    payload = {
        "trainer_code": "TR-DUPLICATE",
        "full_name": "Duplicate Trainer",
        "phone": "03006666666",
        "salary": 40000,
    }

    first_response = client.post(
        "/api/v1/trainers",
        json=payload,
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/api/v1/trainers",
        json=payload,
    )

    assert second_response.status_code == 409


def test_update_trainer():
    response = client.post(
        "/api/v1/trainers",
        json={
            "trainer_code": "TR-UPDATE-001",
            "full_name": "Before Update",
            "phone": "03007777777",
            "salary": 45000,
        },
    )

    assert response.status_code == 201

    trainer_id = response.json()["id"]

    update_response = client.patch(
        f"/api/v1/trainers/{trainer_id}",
        json={
            "full_name": "After Update",
            "salary": 55000,
        },
    )

    assert update_response.status_code == 200

    data = update_response.json()

    assert data["full_name"] == "After Update"
    assert float(data["salary"]) == 55000


def test_deactivate_trainer():
    response = client.post(
        "/api/v1/trainers",
        json={
            "trainer_code": "TR-DEACTIVATE-001",
            "full_name": "Deactivate Trainer",
            "phone": "03008888888",
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