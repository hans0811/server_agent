from flask import Blueprint, jsonify

def setup_routes(app):
    @app.route("/api/get_status", methods=["GET"])
    def get_status():
        return jsonify({"status": "Server is running"}), 200