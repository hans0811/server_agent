import json
import logging
from flask import Flask, request, jsonify
from logging.handlers import RotatingFileHandler

# Constants
AGENT_CONFIG_FILE = "./agent_config.json"
LOG_FILE = "./logs/agent.log"

# Flask app
app = Flask(__name__)

# Configure logging
logger = logging.getLogger("AgentLogger")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(LOG_FILE, maxBytes=5000000, backupCount=3)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


# Load configuration
def load_config():
    try:
        with open(AGENT_CONFIG_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        default_config = {
            "server_version": "v1.0",
            "server_IP": "127.0.0.1",
            "server_port": 5001,
            "schedule": 60
        }
        save_config(default_config)
        return default_config


# Save configuration
def save_config(config):
    with open(AGENT_CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)


# Get installed software (mock different OS)
def get_installed_software(os_type):
    if os_type == "Debian":
        return ["nginx", "mysql-server", "python3"]
    elif os_type == "CentOS":
        return ["httpd", "postgresql", "python3"]
    elif os_type == "Windows":
        return ["Chrome", "VSCode", "Notepad++"]
    return []


# Get agent info (mock different OS)
def get_agent_info(agent_id):
    config = load_config()  # Get latest config
    server_version = config["server_version"]

    agent_data = {
        "A0001": {
            "agent_ID": "A0001",
            "hostname": "debian-agent",
            "ip": "10.100.10.11",
            "os": "Debian",
            "os_version": "11",
            "agent_version": "1.0",
            "server_version": server_version,
            "python_version": "3.9",
            "installed_software": get_installed_software("Debian")
        },
        "A0002": {
            "agent_ID": "A0002",
            "hostname": "centos-agent",
            "ip": "10.100.10.12",
            "os": "CentOS",
            "os_version": "7.9",
            "agent_version": "1.0",
            "server_version": server_version,
            "python_version": "3.6",
            "installed_software": get_installed_software("CentOS")
        },
        "A0003": {
            "agent_ID": "A0003",
            "hostname": "windows-agent",
            "ip": "10.100.10.13",
            "os": "Windows",
            "os_version": "10",
            "agent_version": "1.0",
            "server_version": server_version,
            "python_version": "3.8",
            "installed_software": get_installed_software("Windows")
        }
    }
    return agent_data.get(agent_id, {"error": "Unknown agent ID"})


# API Endpoint: Get agent info
@app.route("/<agent_id>/api/agent_info", methods=["GET"])
def agent_info(agent_id):
    logger.info(f"Received request for {agent_id} info")
    return jsonify(get_agent_info(agent_id))


# API Endpoint: Update configuration
@app.route("/<agent_id>/api/update_config", methods=["POST"])
def update_config(agent_id):
    logger.info(f"Start to update {agent_id} config")
    new_config = request.json
    config = load_config()
    config.update(new_config)
    save_config(config)
    logger.info(f"Configuration updated: {config}")
    return jsonify({"status": "success", "message": "Configuration updated", "new_config": config})


if __name__ == "__main__":
    save_config(load_config())  # Ensure config file exists
    logger.info("Agent started")

    app.run(host="0.0.0.0", port=5002, debug=True)