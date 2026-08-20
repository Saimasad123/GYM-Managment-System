import uuid
from datetime import date, timedelta

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def unique_code(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


def unique_phone() -> str:
    return f"03{uuid.uuid4().int % 10_000_000_000:010d}"


def create_test_member_and_membership(days_until_expiry=10):
    from app.db.session import SessionLocal
    from app.models.member import Member
    from app.models.membership_package import MembershipPackage
    from app.models.membership import Membership

    db_session = SessionLocal()

    try:
        member_code = unique_code("GYM-TEST")
        member = Member(
            member_code=member_code,
            full_name="Test Member",
            phone=unique_phone(),
        )
        db_session.add(member)
        db_session.commit()
        db_session.refresh(member)

        package_name = f"Test Package {uuid.uuid4().hex[:6]}"
        package = MembershipPackage(
            name=package_name,
            duration_months=1,
            price=5000,
            is_active=True,
        )
        db_session.add(package)
        db_session.commit()
        db_session.refresh(package)

        start_date = date.today()
        expiry_date = start_date + timedelta(days=days_until_expiry)

        membership = Membership(
            member_id=member.id,
            package_id=package.id,
            start_date=start_date,
            expiry_date=expiry_date,
            total_fee=package.price,
            amount_paid=package.price,
            status="active",
        )
        db_session.add(membership)
        db_session.commit()
        db_session.refresh(membership)

        return member, package, membership
    finally:
        db_session.close()


def test_get_upcoming_reminders():
    create_test_member_and_membership(days_until_expiry=1)

    response = client.get("/api/v1/reminders/upcoming?days=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1


def test_get_upcoming_reminders_no_results():
    create_test_member_and_membership(days_until_expiry=10)

    response = client.get("/api/v1/reminders/upcoming?days=2")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_create_reminder():
    member, package, membership = create_test_member_and_membership(days_until_expiry=1)

    response = client.post(
        "/api/v1/reminders",
        json={
            "membership_id": membership.id,
            "reminder_date": str(date.today()),
            "reminder_type": "payment_due",
            "message": "Please pay your fees.",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["membership_id"] == membership.id
    assert data["reminder_type"] == "payment_due"


def test_get_reminders():
    create_test_member_and_membership(days_until_expiry=1)

    response = client.get("/api/v1/reminders")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_mark_reminder_sent():
    member, package, membership = create_test_member_and_membership(days_until_expiry=1)

    create_response = client.post(
        "/api/v1/reminders",
        json={
            "membership_id": membership.id,
            "reminder_date": str(date.today()),
            "reminder_type": "payment_due",
            "message": "Please pay your fees.",
        },
    )

    reminder_id = create_response.json()["id"]

    response = client.patch(f"/api/v1/reminders/{reminder_id}/send")
    assert response.status_code == 200
    assert response.json()["is_sent"] is True


def test_get_nonexistent_reminder():
    response = client.patch("/api/v1/reminders/99999/send")
    assert response.status_code == 404
