import pytest
import requests

BASE_URL = "http://127.0.0.1:5002"  # Change if your Flask app runs on a different port


@pytest.fixture(autouse=True)
def reset_config():
    """Reset the agent configuration before each test using the API."""
    default_config = {"server_version": "1.0", "schedule": 60}
    requests.post(f"{BASE_URL}/A0001/api/update_config", json=default_config)
    yield
    requests.post(f"{BASE_URL}/A0001/api/update_config", json=default_config)  # Restore after test


def test_get_agent_info():
    """Test getting agent info for a known agent via API."""
    response = requests.get(f"{BASE_URL}/A0001/api/agent_info")
    assert response.status_code == 200

    data = response.json()
    assert data["agent_id"] == "A0001"
    assert data["os"] == "debian"
    assert "installed_software" in data


def test_update_config():
    """Test updating configuration via API request."""
    new_config = {"server_version": "v1.1", "schedule": 2}

    response = requests.post(f"{BASE_URL}/A0001/api/update_config", json=new_config)
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "success"
    assert data["new_config"]["server_version"] == "v1.1"
    assert data["new_config"]["schedule"] == 2

    # Verify the config was actually updated by making another GET request
    verify_response = requests.get(f"{BASE_URL}/A0001/api/agent_info")
    verify_data = verify_response.json()
    assert verify_data["server_version"] == "v1.1"