import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Arrange & Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data

def test_signup_and_duplicate():
    # Arrange
    activity_name = "Basketball Team"
    email = "athlete@mergington.edu"

    # Act - first signup
    response1 = client.post(f"/activities/{activity_name}/signup?email={email}")
    # Assert
    assert response1.status_code == 200

    # Act - duplicate signup
    response2 = client.post(f"/activities/{activity_name}/signup?email={email}")
    # Assert
    assert response2.status_code == 400
    assert response2.json()["detail"] == "Student is already signed up"

    # Cleanup / Unregister
    response3 = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    assert response3.status_code == 200

def test_signup_nonexistent_activity():
    response = client.post("/activities/NonExistent/signup?email=user@mergington.edu")
    assert response.status_code == 404
