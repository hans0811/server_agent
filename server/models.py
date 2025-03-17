from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Agent:
    """Data class for storing agent details"""
    hostname: str
    ip: str
    os: str
    os_version: str
    agent_version: str
    python_version: str
    installed_software: List[str] = field(default_factory=list)

    @classmethod
    def from_json(cls, data: Dict):
        """Extracts and creates an Agent object from JSON data"""
        return cls(
            hostname=data.get("hostname", "Unknown"),
            ip=data.get("ip", "Unknown"),
            os=data.get("os", "Unknown"),
            os_version=data.get("os_version", "Unknown"),
            agent_version=data.get("agent_version", "Unknown"),
            python_version=data.get("python_version", "Unknown"),
            installed_software=data.get("installed_software", [])
        )