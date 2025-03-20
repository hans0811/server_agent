# Get agent info (mock different OS)
from agent.utility import get_installed_software, load_config


def get_agent_info(agent_id):
    config = load_config()  # Get latest config
    server_version = config["server_version"]

    agent_data = {
        "A0001": {
            "agent_id": "A0001",
            "hostname": "debian-agent",
            "ip": "10.100.10.11",
            "os": "debian",
            "os_version": "11",
            "agent_version": "1.0",
            "server_version": server_version,
            "python_version": "3.9",
            "installed_software": get_installed_software("Debian")
        },
        "A0002": {
            "agent_id": "A0002",
            "hostname": "centos-agent",
            "ip": "10.100.10.12",
            "os": "centos",
            "os_version": "7.9",
            "agent_version": "1.0",
            "server_version": server_version,
            "python_version": "3.6",
            "installed_software": get_installed_software("CentOS")
        },
        "A0003": {
            "agent_id": "A0003",
            "hostname": "windows-agent",
            "ip": "10.100.10.13",
            "os": "windows",
            "os_version": "10",
            "agent_version": "1.0",
            "server_version": server_version,
            "python_version": "3.8",
            "installed_software": get_installed_software("Windows")
        }
    }
    return agent_data.get(agent_id, {"error": "Unknown agent ID"})