# import pytest
# from server import create_app, db
#
# @pytest.fixture
# def app():
#     app = create_app(testing=True)
#     with app.app_context():
#         db.create_all()
#     yield app
#     with app.app_context():
#         db.drop_all()
#
# @pytest.fixture
# def client(app):
#     return app.test_client()