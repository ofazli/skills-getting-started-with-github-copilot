import uuid


def test_at_least_four_activities_are_available(client):
    response = client.get("/activities")

    assert response.status_code == 200
    assert len(response.json()) >= 4


def test_duplicate_signup_is_rejected(client):
    activity_name = "Chess Club"
    email = f"duplicate-{uuid.uuid4().hex}@example.com"

    first_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    second_response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_removes_student_from_activity(client):
    activity_name = "Chess Club"
    email = f"remove-{uuid.uuid4().hex}@example.com"

    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    unregister_response = client.post(f"/activities/{activity_name}/unregister?email={email}")
    activities_response = client.get("/activities")

    assert signup_response.status_code == 200
    assert unregister_response.status_code == 200
    assert email not in activities_response.json()[activity_name]["participants"]