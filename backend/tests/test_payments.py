from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_payment():
    response = client.post(
        "/api/v1/payments",
        json={
            "member_id": 5,
            "amount": 5000,
            "payment_method": "cash",
            "reference_number": "PAY-TEST-001",
            "notes": "Test payment",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["member_id"] == 5
    assert float(data["amount"]) == 5000
    assert data["payment_method"] == "cash"


def test_get_payments():
    response = client.get(
        "/api/v1/payments"
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_member_payments():
    response = client.get(
        "/api/v1/payments/member/5"
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_nonexistent_member_payments():
    response = client.get(
        "/api/v1/payments/member/999999"
    )

    assert response.status_code == 404


def test_create_payment_invalid_member():
    response = client.post(
        "/api/v1/payments",
        json={
            "member_id": 999999,
            "amount": 5000,
            "payment_method": "cash",
        },
    )

    assert response.status_code == 404


def test_get_nonexistent_payment():
    response = client.get(
        "/api/v1/payments/999999"
    )

    assert response.status_code == 404


def test_payment_membership_wrong_member():
    response = client.post(
        "/api/v1/payments",
        json={
            "member_id": 5,
            "membership_id": 999999,
            "amount": 5000,
            "payment_method": "cash",
        },
    )

    assert response.status_code == 404