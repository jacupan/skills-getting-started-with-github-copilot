import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball Team" in data


def test_signup_for_activity():
    email = "newstudent@mergington.edu"
    activity = "Basketball Team"
    # Remove if already present
    client.delete(f"/activities/{activity}/unregister?email={email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]


def test_signup_duplicate():
    email = "alex@mergington.edu"
    activity = "Basketball Team"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_unregister_from_activity():
    email = "alex@mergington.edu"
    activity = "Basketball Team"
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200 or response.status_code == 400
    # Re-add for future tests
    client.post(f"/activities/{activity}/signup?email={email}")


def test_unregister_not_registered():
    email = "notregistered@mergington.edu"
    activity = "Basketball Team"
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]
