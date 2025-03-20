# from flask import Flask
# from model import db  # Ensure the database instance is imported
#
#
# def create_app(testing=False):
#     app = Flask(__name__)
#
#     if testing:
#         app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # ✅ Use in-memory DB for tests
#     else:
#         app.config.from_object("server.config.Config")  # Load normal DB config
#
#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#
#     db.init_app(app)
#
#     with app.app_context():
#         db.create_all()  # ✅ Ensure database tables are created
#
#     # ✅ Register API routes directly in __init__.py if no separate routes file
#     from views import setup_routes
#     setup_routes(app)
#
#     return app
#
#
# # Only run the app when executed directly, NOT when imported
# if __name__ == "__main__":
#     app = create_app()
#     app.run(host="0.0.0.0", port=5001, debug=True)
