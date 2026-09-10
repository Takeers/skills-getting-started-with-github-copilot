from pathlib import Path

from fastapi.testclient import TestClient

from src.app import app


def test_activity_card_js_contains_participants_section_markup_and_refresh_after_signup():
    js_path = Path("src/static/app.js")
    js_text = js_path.read_text()

    assert "participants-list" in js_text
    assert "participants" in js_text
    assert "participant-item" in js_text
    assert "delete-participant" in js_text
    assert "await fetchActivities();" in js_text
    assert "list-style: none" in Path("src/static/styles.css").read_text()


def test_delete_endpoint_unregisters_student():
    client = TestClient(app)

    activity_name = "Soccer Team"
    email = "newstudent@mergington.edu"

    signup_response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    assert signup_response.status_code == 200

    delete_response = client.delete(
        f"/activities/{activity_name}/signup?email={email}"
    )
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == f"Removed {email} from {activity_name}"

    list_response = client.get("/activities")
    assert email not in list_response.json()[activity_name]["participants"]
