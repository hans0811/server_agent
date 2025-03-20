import os


class Config:
    DEBUG = True
    TESTING = True
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret")
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"  # Add this line
    SQLALCHEMY_TRACK_MODIFICATIONS = False
