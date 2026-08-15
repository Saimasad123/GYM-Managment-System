from datetime import date

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_attendance():
    response = client.post(
        "/api/v1/attendance",
        json={
            "member_id": 5,
            "check_in": "09:00:00",
            "status": "present",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["member_id"] == 5
    assert data["status"] == "present"
    assert data["check_in"] == "09:00:00"


def test_get_attendance():
    response = client.get(
        "/api/v1/attendance"
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_today_attendance():
    response = client.get(
        "/api/v1/attendance/today"
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_member_attendance():
    response = client.get(
        "/api/v1/attendance/member/5"
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)

    data = response.json()

    assert all(item["member_id"] == 5 for item in data)


def test_get_nonexistent_member_attendance():
    response = client.get(
        "/api/v1/attendance/member/999999"
    )

    assert response.status_code == 404


def test_duplicate_attendance():
    response = client.post(
        "/api/v1/attendance",
        json={
            "member_id": 6,
            "attendance_date": str(date.today()),
            "check_in": "10:00:00",
            "status": "present",
        },
    )

    assert response.status_code == 201

    duplicate_response = client.post(
        "/api/v1/attendance",
        json={
            "member_id": 6,
            "attendance_date": str(date.today()),
            "check_in": "10:30:00",
            "status": "present",
        },
    )

    assert duplicate_response.status_code == 409


def test_create_attendance_invalid_member():
    response = client.post(
        "/api/v1/attendance",
        json={
            "member_id": 999999,
            "check_in": "09:00:00",
        },
    )

    assert response.status_code == 404


def test_update_attendance():
    response = client.post(
        "/api/v1/attendance",
        json={
            "member_id": 7,
            "check_in": "08:30:00",
            "status": "present",
        },
    )

    assert response.status_code == 201

    attendance_id = response.json()["id"]

    update_response = client.patch(
        f"/api/v1/attendance/{attendance_id}",
        json={
            "check_out": "17:00:00",
        },
    )

    assert update_response.status_code == 200

    data = update_response.json()

    assert data["check_in"] == "08:30:00"
    assert data["check_out"] == "17:00:00"


def test_update_nonexistent_attendance():
    response = client.patch(
        "/api/v1/attendance/999999",
        json={
            "check_out": "17:00:00",
        },
    )

    assert response.status_code == 404
