from datetime import date
import uuid

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def unique_member_code():
    return f"ATT-TEST-{uuid.uuid4().hex[:8]}"


def unique_phone():
    return f"03{uuid.uuid4().int % 10_000_000_000:010d}"


def create_test_member():
    response = client.post(
        "/api/v1/members",
        json={
            "member_code": unique_member_code(),
            "full_name": "Attendance Test Member",
            "phone": unique_phone(),
        },
    )

    assert response.status_code == 201

    return response.json()["id"]


def test_create_attendance():
    member_id = create_test_member()

    response = client.post(
        "/api/v1/attendance",
        json={
            "member_id": member_id,
            "check_in": "09:00:00",
            "status": "present",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["member_id"] == member_id
    assert data["status"] == "present"
    assert data["check_in"] == "09:00:00"


def test_get_attendance():
    response = client.get("/api/v1/attendance")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_today_attendance():
    response = client.get("/api/v1/attendance/today")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_member_attendance():
    member_id = create_test_member()

    create_response = client.post(
        "/api/v1/attendance",
        json={
            "member_id": member_id,
            "check_in": "09:00:00",
            "status": "present",
        },
    )

    assert create_response.status_code == 201

    response = client.get(
        f"/api/v1/attendance/member/{member_id}"
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)

    data = response.json()

    assert all(item["member_id"] == member_id for item in data)


def test_get_nonexistent_member_attendance():
    response = client.get(
        "/api/v1/attendance/member/999999"
    )

    assert response.status_code == 404


def test_duplicate_attendance():
    member_id = create_test_member()

    response = client.post(
        "/api/v1/attendance",
        json={
            "member_id": member_id,
            "attendance_date": str(date.today()),
            "check_in": "10:00:00",
            "status": "present",
        },
    )

    assert response.status_code == 201

    duplicate_response = client.post(
        "/api/v1/attendance",
        json={
            "member_id": member_id,
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
    member_id = create_test_member()

    response = client.post(
        "/api/v1/attendance",
        json={
            "member_id": member_id,
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