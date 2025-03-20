import json
import os
from datetime import datetime

import pytest
import requests

SERVER_URL = "http://127.0.0.1:5001/api"
AGENT_URL = "http://agentFlask:5002"
# Get absolute path of agent_data.json
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get /server/tests
AGENT_DATA_PATH = os.path.join(BASE_DIR, "../agent_data.json")  # Move up to /server


@pytest.fixture(autouse=True)
def reset_config():
    """Reset the agent configuration before and after each test for all agents."""
    default_config = {"server_version": "1.0", "schedule": 60}
    agent_ids = ["A0001", "A0002", "A0003"]

    # Reset before test
    for agent_id in agent_ids:
        requests.post(f"{AGENT_URL}/{agent_id}/api/update_config", json=default_config)

    yield  # Run the test

    # Restore after test
    for agent_id in agent_ids:
        requests.post(f"{AGENT_URL}/{agent_id}/api/update_config", json=default_config)


def test_update_config_then_send_report_debian():
    """Update configuration via Agent API"""
    new_config = {"server_version": "v1.1", "schedule": 2}

    response = requests.post(f"{AGENT_URL}/A0001/api/update_config", json=new_config)
    assert response.status_code == 200

    """Get Agent_Info"""
    response = requests.get(f"{AGENT_URL}/A0001/api/agent_info")
    assert response.status_code == 200

    data = response.json()

    data['timestamp'] = int(datetime.utcnow().timestamp())

    """Report to Server"""
    response = requests.post(f"{SERVER_URL}/agent_report", json=data)
    assert response.status_code == 200

    """Check agent data is update"""
    data_server = {}
    try:
        with open(AGENT_DATA_PATH, "r") as file:
            data_server = json.load(file)
    except FileNotFoundError:
        print("Cannot open")

    assert data_server.get('A0001', {}).get("server_version") == "v1.1"
    assert data_server.get('A0001', {}).get("os") == "debian"


def test_update_config_then_send_report_centos():
    """Update configuration via Agent API"""
    new_config = {"server_version": "v1.1", "schedule": 2}

    response = requests.post(f"{AGENT_URL}/A0002/api/update_config", json=new_config)
    assert response.status_code == 200

    """Get Agent_Info"""
    response = requests.get(f"{AGENT_URL}/A0002/api/agent_info")
    assert response.status_code == 200

    data = response.json()

    data['timestamp'] = int(datetime.utcnow().timestamp())

    """Report to Server"""
    response = requests.post(f"{SERVER_URL}/agent_report", json=data)
    assert response.status_code == 200

    """Check agent data is update"""
    data_server = {}
    try:
        with open(AGENT_DATA_PATH, "r") as file:
            data_server = json.load(file)
    except FileNotFoundError:
        print("Cannot open")

    assert data_server.get('A0002', {}).get("server_version") == "v1.1"
    assert data_server.get('A0002', {}).get("os") == "centos"


def test_update_config_then_send_report_windows():
    """Update configuration via Agent API"""
    new_config = {"server_version": "v1.1", "schedule": 2}

    response = requests.post(f"{AGENT_URL}/A0003/api/update_config", json=new_config)
    assert response.status_code == 200

    """Get Agent_Info"""
    response = requests.get(f"{AGENT_URL}/A0003/api/agent_info")
    assert response.status_code == 200

    data = response.json()

    data['timestamp'] = int(datetime.utcnow().timestamp())

    """Report to Server"""
    response = requests.post(f"{SERVER_URL}/agent_report", json=data)
    assert response.status_code == 200

    """Check agent data is update"""
    data_server = {}
    try:
        with open(AGENT_DATA_PATH, "r") as file:
            data_server = json.load(file)
    except FileNotFoundError:
        print("Cannot open")

    assert data_server.get('A0003', {}).get("server_version") == "v1.1"
    assert data_server.get('A0003', {}).get("os") == "windows"

