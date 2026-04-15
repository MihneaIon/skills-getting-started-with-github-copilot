from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

def test_get_activities_returns_activities():
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert expected_activity in data
    assert data[expected_activity]["description"] == activities[expected_activity]["description"]


def test_signup_for_activity_adds_participant():
    # Arrange
    activity_name = "Tennis Club"
    email = "newstudent@mergington.edu"
    payload = {"email": email}
    original_participants = list(activities[activity_name]["participants"])

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params=payload)

    # Assert
    assert response.status_code == 200
    assert email in activities[activity_name]["participants"]
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}

    # Cleanup
    activities[activity_name]["participants"] = original_participants


def test_duplicate_signup_returns_400():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    payload = {"email": email}

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params=payload)

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_remove_participant_from_activity():
    # Arrange
    activity_name = "Basketball Team"
    email = "alex@mergington.edu"
    payload = {"email": email}
    original_participants = list(activities[activity_name]["participants"])

    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params=payload)

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from {activity_name}"}
    assert email not in activities[activity_name]["participants"]

    # Cleanup
    activities[activity_name]["participants"] = original_participants


def test_remove_missing_participant_returns_404():
    # Arrange
    activity_name = "Chess Club"
    email = "missingstudent@mergington.edu"
    payload = {"email": email}

    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params=payload)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"


def test_remove_from_unknown_activity_returns_404():
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"
    payload = {"email": email}

    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params=payload)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
