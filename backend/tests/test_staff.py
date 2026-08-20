import uuid

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def unique_code(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


def test_create_staff():
    response = client.post(
        "/api/v1/staff",
        json={
            "staff_code": unique_code("STF"),
            "full_name": "John Doe",
            "phone": f"03{uuid.uuid4().int % 10_000_000_000:010d}",
            "role": "Receptionist",
            "salary": 25000,
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["full_name"] == "John Doe"
    assert data["is_active"] is True


def test_get_staff():
    client.post(
        "/api/v1/staff",
        json={
            "staff_code": unique_code("STF"),
            "full_name": "Jane Smith",
            "phone": f"03{uuid.uuid4().int % 10_000_000_000:010d}",
            "role": "Manager",
        },
    )

    response = client.get("/api/v1/staff")
    assert response.status_code == 200
    assert len(response.json()) >= 2


def test_get_active_staff():
    response = client.get("/api/v1/staff/active")
    assert response.status_code == 200


def test_get_staff_member():
    create_response = client.post(
        "/api/v1/staff",
        json={
            "staff_code": unique_code("STF"),
            "full_name": "Bob Johnson",
            "phone": f"03{uuid.uuid4().int % 10_000_000_000:010d}",
            "role": "Cleaner",
        },
    )
    staff_id = create_response.json()["id"]

    response = client.get(f"/api/v1/staff/{staff_id}")
    assert response.status_code == 200
    assert response.json()["full_name"] == "Bob Johnson"


def test_get_nonexistent_staff():
    response = client.get("/api/v1/staff/99999")
    assert response.status_code == 404


def test_duplicate_staff_code():
    code = unique_code("STF-DUP")

    client.post(
        "/api/v1/staff",
        json={
            "staff_code": code,
            "full_name": "First",
            "phone": f"03{uuid.uuid4().int % 10_000_000_000:010d}",
            "role": "Receptionist",
        },
    )

    response = client.post(
        "/api/v1/staff",
        json={
            "staff_code": code,
            "full_name": "Second",
            "phone": f"03{uuid.uuid4().int % 10_000_000_000:010d}",
            "role": "Manager",
        },
    )

    assert response.status_code == 400


def test_update_staff():
    create_response = client.post(
        "/api/v1/staff",
        json={
            "staff_code": unique_code("STF"),
            "full_name": "Before Update",
            "phone": f"03{uuid.uuid4().int % 10_000_000_000:010d}",
            "role": "Receptionist",
        },
    )
    staff_id = create_response.json()["id"]

    response = client.patch(
        f"/api/v1/staff/{staff_id}",
        json={"full_name": "After Update"},
    )
    assert response.status_code == 200
    assert response.json()["full_name"] == "After Update"


def test_deactivate_staff():
    create_response = client.post(
        "/api/v1/staff",
        json={
            "staff_code": unique_code("STF"),
            "full_name": "Deactivate Staff",
            "phone": f"03{uuid.uuid4().int % 10_000_000_000:010d}",
            "role": "Manager",
        },
    )
    staff_id = create_response.json()["id"]

    response = client.delete(f"/api/v1/staff/{staff_id}")
    assert response.status_code == 204

    get_response = client.get(f"/api/v1/staff/{staff_id}")
    assert get_response.status_code == 200
    assert get_response.json()["is_active"] is False
