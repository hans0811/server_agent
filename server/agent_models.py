import json
import os
import uuid
from datetime import datetime
from uuid import UUID

from flask_sqlalchemy import SQLAlchemy
from pydantic import BaseModel, ValidationError, field_validator, validator
from typing import List
from sqlalchemy.dialects.postgresql import JSON

db = SQLAlchemy()


class AgentModel(db.Model):
    """SQLAlchemy model for database structure."""
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    hostname = db.Column(db.String(100), nullable=False)
    ip = db.Column(db.String(15), nullable=False)
    os = db.Column(db.String(50), nullable=False)
    os_version = db.Column(db.String(50), nullable=False)
    python_version = db.Column(db.String(10), nullable=False)
    installed_software = db.Column(JSON)  # Stored as JSON string


class AgentSchema(BaseModel):
    """Pydantic model for strict data validation."""
    agent_id: str
    hostname: str
    ip: str
    os: str
    os_version: str
    server_version: str
    python_version: str
    installed_software: List[str]
    timestamp: str

    @field_validator("timestamp", mode="before")
    @classmethod
    def convert_unix_to_datetime(cls, value):
        """Automatically convert Unix timestamp to datetime string"""
        print(value)
        return datetime.utcfromtimestamp(value).strftime('%Y-%m-%d %H:%M:%S')


def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    return {}


# Save data to file
def save_data(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)
