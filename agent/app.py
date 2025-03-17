import json
import socket
import platform
import subprocess
import requests

SERVER_URL = "http://localhost:5001/api/agent_report"


def get_installed_software():
    """Detect installed software based on OS type"""
    software_list = []
    try:
        if platform.system() == "Linux":
            if subprocess.run(["which", "dpkg"], stdout=subprocess.DEVNULL).returncode == 0:
                result = subprocess.run(["dpkg", "--list"], capture_output=True, text=True)
                software_list = [line.split()[1] for line in result.stdout.splitlines()[5:] if len(line.split()) > 1]
            elif subprocess.run(["which", "rpm"], stdout=subprocess.DEVNULL).returncode == 0:
                result = subprocess.run(["rpm", "-qa"], capture_output=True, text=True)
                software_list = result.stdout.splitlines()
        elif platform.system() == "Windows":
            result = subprocess.run(["winget", "list"], capture_output=True, text=True)
            software_list = [line.split()[0] for line in result.stdout.splitlines()[3:] if len(line.split()) > 1]
    except Exception as e:
        print(f"Error detecting installed software: {e}")

    return software_list


def get_agent_info():
    """Collect system and software information"""
    return {
        "hostname": socket.gethostname(),
        "ip": socket.gethostbyname(socket.gethostname()),
        "os": platform.system(),
        "os_version": platform.version(),
        "python_version": platform.python_version(),
        "installed_software": get_installed_software()
    }

def get_agent_info_mock():
    """Collect system and software information"""
    return {
        "hostname": "3.7",
        "ip": "10.100.10.7",
        "os": "centos",
        "os_version": "7.8",
        "agent_version": "1.0",
        "python_version": "3.7",
        "python_version1": 0,
        "installed_software": ["jenkins","docker"]
    }


def send_data():
    """Send agent info to the server"""
    data = get_agent_info_mock()
    try:
        response = requests.post(SERVER_URL, json=data)
        print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error sending data: {e}")


if __name__ == "__main__":
    send_data()
