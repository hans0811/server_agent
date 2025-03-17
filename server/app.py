from flask import Flask, request, jsonify, app
from dataclasses import dataclass, field
from typing import List, Dict

from server.models import Agent

app = Flask(__name__)

# Mock database
agents_db = []


@app.route("/api/agent_report", methods=["POST"])
def agent_report():
    """Receive and store agent data"""
    data = request.get_json()
    agent = Agent.from_json(data)  # Convert JSON to Agent object
    agents_db.append(agent)
    return jsonify({"status": "ok", "message": "Agent data received"}), 200


@app.route("/api/agents", methods=["GET"])
def get_agents():
    """Retrieve all agents as JSON"""
    return jsonify([agent.__dict__ for agent in agents_db]), 200


@app.route("/api/agent/<hostname>", methods=["GET"])
def get_agent_details(hostname):
    """Retrieve details of a specific agent"""
    agent = next((a for a in agents_db if a.hostname == hostname), None)
    if agent:
        return jsonify(agent.__dict__), 200
    return jsonify({"error": "Agent not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
