import logging
import os

import requests
from flask import Flask, request, jsonify
from pydantic import ValidationError

from agent_models import AgentSchema, load_data, save_data

# Constants
AGENT_DATA_FILE = "agent_data.json"
AGENT_URL = "http://agentFlask:5002"

log_dir = "logs"


logging.basicConfig(
    filename="'server.log'",  # Save logs inside logs/
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def create_app():
    """Create and configure the Flask app."""
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"  # Persistent SQLite
    # app.config.from_object(Config)
    # db.init_app(app)

    logging.info("Starting run app...")

    # with app.app_context():
    #     db.create_all()  # Ensure tables exist

    @app.route("/api/get_status", methods=["GET"])
    def server_status():
        return jsonify({"status": "ok", "message": "Server Healthy"}), 200

    @app.route("/api/agent_report", methods=["POST"])
    def agent_report():
        """Receive and validate agent data using Pydantic and store in JSON file."""
        try:
            data = request.get_json()
            if not data:
                logging.warning("Received empty JSON request")
                return jsonify({"error": "No JSON received"}), 400

            # Validate data with Pydantic
            agent_data = AgentSchema(**data)

            # Load existing data
            agent_store = load_data(AGENT_DATA_FILE)

            # Save new agent data
            agent_store[agent_data.agent_id] = agent_data.model_dump()
            save_data(AGENT_DATA_FILE, agent_store)

            logging.info(f"Agent data saved: {agent_data}")
            return jsonify({"status": "ok", "message": "Agent data received"}), 200

        except ValidationError as e:
            logging.error(f"Validation error: {e}")
            return jsonify({"error": e.errors()}), 400
        except Exception as e:
            logging.critical(f"Unexpected error: {e}", exc_info=True)
            return jsonify({"error": "Unexpected error occurred"}), 500

    @app.route("/api/update_agent_config", methods=["POST"])
    def update_gent_config():
        """Server calls agent API to update config"""
        data = request.get_json()
        agent_id = data.get("agent_id")
        new_config = data.get("config")

        if not agent_id or not new_config:
            return jsonify({"error": "Missing agent_id or config"}), 400

        result = update_agent_config(agent_id, new_config)
        return jsonify(result)
    return app

def update_agent_config(agent_id, new_config):
    """Update the agent's configuration via API."""
    url = f"{AGENT_URL}/{agent_id}/api/update_config"
    try:
        response = requests.post(url, json=new_config)
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.json()
    except requests.RequestException as e:
        return {"error": f"Failed to update agent {agent_id}: {str(e)}"}


if __name__ == "__main__":
    app = create_app()
    logging.info("Starting server...")
    app.run(host="0.0.0.0", port=5001, debug=True)
