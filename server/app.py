import logging
import os

from flask import Flask, request, jsonify
from pydantic import ValidationError

from agent_models import AgentSchema, load_data, save_data

# Constants
AGENT_DATA_FILE = "agent_data.json"

log_dir = "logs"
#os.makedirs(log_dir, exist_ok=True)  # Ensure the logs directory exists

logging.basicConfig(
    filename="'server/logs/server.log'",  # Save logs inside logs/
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def create_app():
    """Create and configure the Flask app."""
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"  # Persistent SQLite
    # app.config.from_object(Config)
    #db.init_app(app)

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

    return app


if __name__ == "__main__":
    app = create_app()
    logging.info("Starting server...")
    app.run(host="0.0.0.0", port=5001, debug=True)
