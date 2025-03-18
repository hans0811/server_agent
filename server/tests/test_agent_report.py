import requests
import json

# Configuration for API URLs
BASE_URL = "http://127.0.0.1:5001/api"
STATUS_URL = f"{BASE_URL}/get_status"
AGENT_REPORT_URL = f"{BASE_URL}/agent_report"

def test_aserver_status():
    """Test API with valid server data."""
    response = requests.get(STATUS_URL)
    assert response.status_code == 200

    response_dict = json.loads(response.text)  # Convert response text to dictionary
    assert "status" in response_dict
    assert response_dict["status"] == "ok"

def test_valid_agent_report():
    """Test API with valid agent data."""
    payload = {
        "hostname": "test.com",
        "agent_id": "123",
        "os": "Linux",
        "os_version": "Ubuntu 20.04",
        "ip": "192.168.1.100",
        "python_version": "3.9",
        "installed_software": ["jenkins", 'docker']
    }
    response = requests.post(AGENT_REPORT_URL, json=payload)
    assert response.status_code == 200

    response_dict = json.loads(response.text)
    assert response_dict["message"] == "Agent data received"

def test_invalid_os():
    """Test API with invalid OS data."""
    payload = {
        "agent_id": "123",
        "os": "InvalidOS",
        "os_version": "Ubuntu 20.04",
        "ip": "192.168.1.100"
    }
    response = requests.post(AGENT_REPORT_URL, json=payload)
    assert response.status_code == 400  # Expecting a bad request

    response_dict = json.loads(response.text)
    assert "error" in response_dict

def test_missing_fields():
    """Test API with missing required fields."""
    payload = {
        "agent_id": "123",
        "os": "Linux"
        # Missing os_version and ip
    }
    response = requests.post(AGENT_REPORT_URL, json=payload)
    assert response.status_code == 400  # Expecting a bad request

    response_dict = json.loads(response.text)
    assert "error" in response_dict