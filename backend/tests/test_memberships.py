from datetime import date

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def create_test_member():
    response = client.post(
        "/api/v1/members",
        json={
            "member_code": "GYM-MEMBERSHIP-001",
            "full_name": "Membership Test Member",
            "phone": "03009999999",
        },
    )

    if response.status_code == 409:
        members = client.get("/api/v1/members").json()

        for member in members:
            if member["member_code"] == "GYM-MEMBERSHIP-001":
                return member["id"]

    assert response.status_code == 201

    return response.json()["id"]


def create_test_package():
    response = client.post(
        "/api/v1/membership-packages",
        json={
            "name": "Test Monthly Package",
            "duration_months": 1,
            "price": 5000,
            "description": "Package for automated tests",
        },
    )

    if response.status_code == 409:
        packages = client.get(
            "/api/v1/membership-packages"
        ).json()

        for package in packages:
            if package["name"] == "Test Monthly Package":
                return package["id"]

    assert response.status_code == 201

    return response.json()["id"]


def test_create_membership():
    member_id = create_test_member()
    package_id = create_test_package()

    response = client.post(
        "/api/v1/memberships",
        json={
            "member_id": member_id,
            "package_id": package_id,
            "start_date": "2026-08-14",
            "amount_paid": 3000,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["member_id"] == member_id
    assert data["package_id"] == package_id
    assert data["start_date"] == "2026-08-14"
    assert data["expiry_date"] == "2026-09-14"
    assert float(data["total_fee"]) == 5000
    assert float(data["amount_paid"]) == 3000
    assert data["status"] == "active"


def test_get_memberships():
    response = client.get(
        "/api/v1/memberships"
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_active_memberships():
    response = client.get(
        "/api/v1/memberships/active"
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_membership_invalid_member():
    package_id = create_test_package()

    response = client.post(
        "/api/v1/memberships",
        json={
            "member_id": 999999,
            "package_id": package_id,
            "start_date": "2026-08-14",
            "amount_paid": 0,
        },
    )

    assert response.status_code == 404


def test_create_membership_invalid_package():
    member_id = create_test_member()

    response = client.post(
        "/api/v1/memberships",
        json={
            "member_id": member_id,
            "package_id": 999999,
            "start_date": "2026-08-14",
            "amount_paid": 0,
        },
    )

    assert response.status_code == 404


def test_amount_paid_cannot_exceed_fee():
    member_id = create_test_member()
    package_id = create_test_package()

    response = client.post(
        "/api/v1/memberships",
        json={
            "member_id": member_id,
            "package_id": package_id,
            "start_date": "2026-08-14",
            "amount_paid": 6000,
        },
    )

    assert response.status_code == 400


def test_get_nonexistent_membership():
    response = client.get(
        "/api/v1/memberships/999999"
    )

    assert response.status_code == 404
