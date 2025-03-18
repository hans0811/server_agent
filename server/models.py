from flask_sqlalchemy import SQLAlchemy
from pydantic import BaseModel, ValidationError
from typing import List

db = SQLAlchemy()


class AgentModel(db.Model):
    """SQLAlchemy model for database structure."""
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(100), nullable=False)
    ip = db.Column(db.String(15), nullable=False)
    os = db.Column(db.String(50), nullable=False)
    os_version = db.Column(db.String(50), nullable=False)
    python_version = db.Column(db.String(10), nullable=False)
    installed_software = db.Column(db.String(500))  # Stored as JSON string


class AgentSchema(BaseModel):
    """Pydantic model for strict data validation."""
    hostname: str
    ip: str
    os: str
    os_version: str
    python_version: str
    installed_software: List[str]
