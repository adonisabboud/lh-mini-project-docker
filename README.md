# Dockerized Flask App with Ansible Deployment

A Flask REST API backed by PostgreSQL, fully containerized with Docker and automated using Ansible for multi-node deployment.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Ansible Master                       │
│              (orchestrates deployment)                  │
│                     │                                   │
│           ┌─────────┴─────────┐                         │
│           ▼                   ▼                         │
│    ┌─────────────┐   ┌──────────────┐                  │
│    │  Slave 1    │   │   Slave 2    │                  │
│    │  (App Host) │   │  (DB Host)   │                  │
│    │             │   │              │                  │
│    │  Flask API  │   │  PostgreSQL  │                  │
│    │  :5000      │   │  :5432       │                  │
│    │             │   │  pgAdmin     │                  │
│    │             │   │  :8080       │                  │
│    └─────────────┘   └──────────────┘                  │
│           │                   │                         │
│           └───── app-net ─────┘                         │
└─────────────────────────────────────────────────────────┘
```

The setup simulates a two-server deployment using Docker containers as Ansible-managed nodes:

- **Slave 1** runs the Flask application container
- **Slave 2** runs PostgreSQL and pgAdmin containers
- **Master** connects to both slaves via SSH and runs the Ansible playbook

All application containers communicate over a shared `app-net` Docker network.

## Project Structure

```
.
├── ansible/                    # Ansible configuration
│   ├── deploy.yml              # Main deployment playbook
│   ├── docker-compose.yml      # Ansible master + slave containers
│   ├── inventory.ini           # Host inventory
│   └── group_vars/all/         # Variables and encrypted vault
├── ansible-master/
│   └── Dockerfile              # Ansible control node image
├── ansible-slave/
│   └── Dockerfile              # Managed node image (Ubuntu + SSH + Docker)
├── app/
│   ├── Dockerfile              # Flask app image
│   ├── docker-compose.yml      # App service definition
│   └── src/
│       ├── app.py              # Flask application
│       └── requirements.txt    # Python dependencies
├── database/
│   ├── docker-compose.yml      # PostgreSQL + pgAdmin services
│   └── init.sql                # Database schema and seed data
├── ansible_key                 # SSH key pair for Ansible (gitignored)
└── ansible_key.pub
```

## API Endpoints

| Method | Endpoint   | Description            |
|--------|------------|------------------------|
| GET    | `/users`   | List all users         |
| POST   | `/users`   | Create a new user      |
| GET    | `/health`  | Database health check  |

### Create a user

```bash
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"username": "charlie", "email": "charlie@example.com", "password": "pass789"}'
```

### List users

```bash
curl http://localhost:5000/users
```

## Tech Stack

- **Application:** Python 3.11, Flask
- **Database:** PostgreSQL 15
- **DB Admin:** pgAdmin 4 (available on port 8080)
- **Containerization:** Docker, Docker Compose
- **Automation:** Ansible
- **Ansible Images:** Pre-built on DockerHub (`adonisabboud/mini-prj-ansible`)

## Getting Started

### Prerequisites

- Docker and Docker Compose
- An SSH key pair for Ansible (place `ansible_key` and `ansible_key.pub` in the project root)

### 1. Start the Ansible infrastructure

```bash
cd ansible
docker compose up -d
```

This starts the Ansible master and two slave containers.

### 2. Run the deployment playbook

```bash
docker exec -it ansible-master bash
ansible-playbook -i inventory.ini deploy.yml --ask-vault-pass
```

The playbook will:
1. Clone the repo on each slave
2. Create `.env` files from Ansible vault secrets
3. Start the database on Slave 2 and wait for it to be ready
4. Build and start the Flask app on Slave 1

### 3. Verify

```bash
# Health check
curl http://localhost:5000/health

# List seeded users
curl http://localhost:5000/users
```

pgAdmin is accessible at `http://localhost:8080` (credentials configured in the database `.env`).

## Sensitive Data

Passwords and secrets are managed with Ansible Vault (`ansible/group_vars/all/vault.yml`). The `.env` files and SSH keys are gitignored.
