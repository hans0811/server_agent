import logging
from flask import Flask, request, jsonify
from models import db, AgentModel, AgentSchema
from pydantic import ValidationError
from config import Config

# Configure logging
logging.basicConfig(
    filename="server.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def create_app():
    """Create and configure the Flask app."""
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"  # Persistent SQLite
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        db.create_all()  # Ensure tables exist

    @app.route("/api/get_status", methods=["GET"])
    def server_status():
        return jsonify({"status": "ok", "message": "Server Healthy"}), 200

    @app.route("/api/agent_report", methods=["POST"])
    def agent_report():
        """Receive and validate agent data using Pydantic & SQLAlchemy."""
        try:
            data = request.get_json()
            if not data:
                logging.warning("Received empty JSON request")
                return jsonify({"error": "No JSON received"}), 400

            # Validate data with Pydantic
            agent_data = AgentSchema(**data)

            # Store in the database
            agent = AgentModel(
                hostname=agent_data.hostname,
                ip=agent_data.ip,
                os=agent_data.os,
                os_version=agent_data.os_version,
                python_version=agent_data.python_version,
                installed_software=",".join(agent_data.installed_software),
            )
            db.session.add(agent)
            db.session.commit()

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