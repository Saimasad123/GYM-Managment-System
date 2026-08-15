
import uuid

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def unique_code(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


def unique_phone() -> str:
    return f"03{uuid.uuid4().int % 10_000_000_000:010d}"


def test_create_member():
    code = unique_code("GYM-TEST")
    phone = unique_phone()

    response = client.post(
        "/api/v1/members",
        json={
            "member_code": code,
            "full_name": "Test Member",
            "father_name": "Test Father",
            "phone": phone,
            "cnic": None,
            "gender": "Male",
            "address": "Karachi",
            "emergency_contact": "03007654321",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["member_code"] == code
    assert data["full_name"] == "Test Member"
    assert data["is_active"] is True


def test_get_members():
    response = client.get(
        "/api/v1/members"
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_active_members():
    response = client.get(
        "/api/v1/members/active"
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_nonexistent_member():
    response = client.get(
        "/api/v1/members/999999"
    )

    assert response.status_code == 404


def test_duplicate_member_code():
    code = unique_code("GYM-DUPLICATE")

    first_payload = {
        "member_code": code,
        "full_name": "Duplicate Test",
        "phone": unique_phone(),
    }

    first_response = client.post(
        "/api/v1/members",
        json=first_payload,
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/api/v1/members",
        json=first_payload,
    )

    assert second_response.status_code == 409


def test_update_member():
    response = client.post(
        "/api/v1/members",
        json={
            "member_code": unique_code("GYM-UPDATE"),
            "full_name": "Before Update",
            "phone": unique_phone(),
        },
    )

    assert response.status_code == 201

    member_id = response.json()["id"]

    update_response = client.patch(
        f"/api/v1/members/{member_id}",
        json={
            "full_name": "After Update",
            "phone": unique_phone(),
        },
    )

    assert update_response.status_code == 200

    data = update_response.json()

    assert data["full_name"] == "After Update"


def test_deactivate_member():
    response = client.post(
        "/api/v1/members",
        json={
            "member_code": unique_code("GYM-DEACTIVATE"),
            "full_name": "Deactivate Test",
            "phone": unique_phone(),
        },
    )

    assert response.status_code == 201

    member_id = response.json()["id"]

    delete_response = client.delete(
        f"/api/v1/members/{member_id}"
    )

    assert delete_response.status_code == 200
    assert delete_response.json()["is_active"] is False
