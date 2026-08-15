from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_dashboard_summary():
    response = client.get(
        "/api/v1/dashboard/summary"
    )

    assert response.status_code == 200

    data = response.json()

    assert "total_members" in data
    assert "active_members" in data
    assert "expired_memberships" in data
    assert "today_revenue" in data
    assert "monthly_revenue" in data
    assert "total_memberships" in data


def test_dashboard_summary_types():
    response = client.get(
        "/api/v1/dashboard/summary"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data["total_members"], int)
    assert isinstance(data["active_members"], int)
    assert isinstance(data["expired_memberships"], int)
    assert isinstance(data["total_memberships"], int)