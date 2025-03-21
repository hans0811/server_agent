# Server-Agent Flask Application

This project consists of a **Server** and multiple **Agents** that communicate via RESTful APIs. The **Server** updates agent configurations and collects agent reports. Both services are containerized using **Docker** and managed via **Docker Compose**.

## Features

- **Server**
  - Updates agent configurations via `/api/update_config`
  - Receives agent reports via `/api/agent_report`

- **Agent**
  - Receives configuration updates from the server
  - Sends system reports back to the server

- **Docker Support**
  - Prebuilt images available on Docker Hub
  - Easy deployment with `docker-compose`

---

## Tech Stack

1. Python 3.9 - Flask
2. Jenkins
3. Docker
---

## Project Structure
```
CICD/
│── agent/                # Agent component
│   │── logs/             # Agent logs
│   │── agent_mock.py     # Simulated agent for testing
│   │── app.py            # Main agent script
│   │── dockerfile        # Docker setup for agent
│   │── requirements.txt  # Dependencies
│   │── utility.py        # Helper functions
│
│── server/               # Server component
│   │── logs/             # Server logs
│   │── tests/            # Unit tests
│   │── app.py            # Main server script
│   │── config.py         # Configuration settings
│   │── views.py          # API routes
│   │── dockerfile        # Docker setup for server
│   │── requirements.txt  # Dependencies
│
│── CI/                   # CI/CD Pipeline setup
│   │── jenkinsfile.groovy# Jenkins pipeline script
│
│── docker-compose.yml    # Docker Compose configuration
│── README.md             # Project documentation
```

---

## Setup & Deployment

### Clone Repository
```sh
git clone https://github.com/hans0811/server_agent/tree/master
```


### Quick Deploy
```sh
docker-compose up
```

### PyTest
```sh
pytest -s ./tests/ --disable-warnings -v
```
