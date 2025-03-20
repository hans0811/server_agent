import json
import logging
from flask import Flask, request, jsonify
from logging.handlers import RotatingFileHandler

from agent.agent_mock import get_agent_info
from agent.utility import load_config, get_installed_software, save_config

# Constants
LOG_FILE = "./agent.log"

# Flask app
app = Flask(__name__)

# Configure logging
logger = logging.getLogger("AgentLogger")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(LOG_FILE, maxBytes=5000000, backupCount=3)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


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