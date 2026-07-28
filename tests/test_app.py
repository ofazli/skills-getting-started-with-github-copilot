import uuid

from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_at_least_four_activities_are_available():
    response = client.get("/activities")

    assert response.status_code == 200
    assert len(response.json()) >= 4


def test_duplicate_signup_is_rejected():
    activity_name = "Chess Club"
    email = f"duplicate-{uuid.uuid4().hex}@example.com"

    first_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    second_response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student already signed up for this activity"
