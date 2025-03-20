import json

# Constants
AGENT_CONFIG_FILE = "./agent_config.json"



# Load configuration
def load_config():
    try:
        with open(AGENT_CONFIG_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        default_config = {
            "server_version": "v1.0",
            "server_IP": "127.0.0.1",
            "server_port": 5001,
            "schedule": 60
        }
        save_config(default_config)
        return default_config


# Save configuration
def save_config(config):
    with open(AGENT_CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)


# Get installed software (mock different OS)
def get_installed_software(os_type):
    if os_type == "Debian":
        return ["nginx", "mysql-server", "python3"]
    elif os_type == "CentOS":
        return ["httpd", "postgresql", "python3"]
    elif os_type == "Windows":
        return ["Chrome", "VSCode", "Notepad++"]
    return []
