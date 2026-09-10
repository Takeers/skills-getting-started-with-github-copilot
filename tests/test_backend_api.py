import uuid

from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_get_activities_returns_activity_collection():
    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert "Programming Class" in payload
    assert "Gym Class" in payload


def test_signup_duplicate_and_delete_flow():
    activity_name = "Soccer Team"
    email = f"student{uuid.uuid4().hex}@mergington.edu"

    post_response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    assert post_response.status_code == 200
    assert post_response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in activities[activity_name]["participants"]

    duplicate_response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    assert duplicate_response.status_code == 400
    assert "already signed up" in duplicate_response.json()["detail"].lower()

    delete_response = client.delete(
        f"/activities/{activity_name}/signup?email={email}"
    )
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == f"Removed {email} from {activity_name}"
    assert email not in activities[activity_name]["participants"]
