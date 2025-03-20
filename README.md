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

## 📦 Setup & Deployment

### 1️⃣ Clone Repository
```sh
git clone https://github.com/your-repo/server-agent.git
cd server-agent




sudo vi /etc/docker/daemon.json