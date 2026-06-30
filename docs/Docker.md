# Docker Guide for the RAG Application

## Overview

This project uses **Docker** to package and run all required components of the application. Instead of installing PostgreSQL, Ollama, Python, and all dependencies manually on every machine, Docker creates isolated environments called **containers**.

The application consists of three containers:

1. **PostgreSQL + pgvector** – Stores application data and vector embeddings.
2. **Ollama** – Hosts the Large Language Model (LLM).
3. **FastAPI** – Provides the REST API and orchestrates communication between PostgreSQL and Ollama.

---

# What is Docker?

Docker packages an application along with all its dependencies into a **container**.

Think of a container as a lightweight virtual machine that already contains:

- Operating System libraries
- Python
- Required packages
- Application code
- Runtime configuration

Instead of asking every developer to install everything manually, Docker ensures that everyone runs the exact same environment.

---

# Project Architecture

```
                   Browser / Client
                          │
                    localhost:8000
                          │
                  +----------------+
                  |    FastAPI     |
                  |   REST APIs    |
                  +----------------+
                     │          │
                     │          │
                     ▼          ▼
             +--------------+  +--------------+
             | PostgreSQL   |  |    Ollama    |
             | + pgvector   |  |     LLM      |
             +--------------+  +--------------+
```

The FastAPI application receives requests from clients and communicates with:

- PostgreSQL for storing/retrieving data
- Ollama for interacting with the language model

---

# Docker Compose

The `docker-compose.yml` file describes the complete application.

Instead of starting each container manually, Docker Compose starts everything with a single command.

```bash
docker compose up
```

The compose file contains three services:

- postgres
- ollama
- fastapi

---

# Understanding the Docker Compose File

## Version

```yaml
version: "3.9"
```

This specifies the Docker Compose specification version.

Modern Docker versions generally infer this automatically, but it is still commonly included.

---

# Services

```yaml
services:
```

A **service** represents one container.

Our application contains:

```
services
│
├── postgres
├── ollama
└── fastapi
```

---

# PostgreSQL Service

```yaml
postgres:
```

This starts a PostgreSQL database with the pgvector extension.

## Image

```yaml
image: pgvector/pgvector:pg16
```

Docker downloads an existing PostgreSQL image that already contains the pgvector extension.

Think of an image as a reusable blueprint for creating containers.

---

## Container Name

```yaml
container_name: pgvector-db
```

Instead of assigning a random name, Docker names the container:

```
pgvector-db
```

---

## Restart Policy

```yaml
restart: always
```

If the container crashes or Docker restarts, the database starts automatically.

---

## Environment Variables

```yaml
environment:

  POSTGRES_DB: ragdb

  POSTGRES_USER: admin

  POSTGRES_PASSWORD: admin123
```

These values initialize PostgreSQL.

| Variable | Value |
|----------|-------|
| Database | ragdb |
| Username | admin |
| Password | admin123 |

---

## Port Mapping

```yaml
ports:

  - "5432:5432"
```

Format:

```
HOST_PORT : CONTAINER_PORT
```

Meaning:

```
Your Computer          PostgreSQL Container

localhost:5432   --->      5432
```

Applications outside Docker can connect using:

```
localhost:5432
```

---

## Volumes

```yaml
volumes:

  - postgres_data:/var/lib/postgresql/data
```

Without volumes:

Stopping or deleting the container would delete the database.

Volumes store data outside the container.

```
Container

Database Files
       │
       ▼
Docker Volume
       │
       ▼
Persistent Storage
```

---

# Ollama Service

```yaml
ollama:
```

Runs the Ollama server.

---

## Image

```yaml
image: ollama/ollama
```

Downloads the official Ollama image.

---

## Port

```yaml
11434:11434
```

The Ollama API becomes available at:

```
http://localhost:11434
```

---

## Volume

```yaml
ollama:/root/.ollama
```

Downloaded models (Llama, Mistral, Phi, etc.) are stored here.

Without this volume, models would need to be downloaded every time the container is recreated.

---

# FastAPI Service

```yaml
fastapi:
```

This is the main application.

Unlike PostgreSQL and Ollama, this container is built from the project source code.

---

## Build

```yaml
build: .
```

Docker looks for a file named:

```
Dockerfile
```

inside the current directory and builds the application image.

---

## Depends On

```yaml
depends_on:

  - postgres

  - ollama
```

Docker starts containers in this order:

```
PostgreSQL
      │
      ▼
Ollama
      │
      ▼
FastAPI
```

> **Note:** `depends_on` controls startup order but does not guarantee that PostgreSQL or Ollama are fully ready to accept connections.

---

## Port Mapping

```yaml
8000:8000
```

The FastAPI application is available at:

```
http://localhost:8000
```

---

## Environment Variables

```yaml
POSTGRES_DB=ragdb
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin123
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
```

These values are available inside the Python application.

Example:

```python
import os

host = os.getenv("POSTGRES_HOST")
```

Notice:

```
POSTGRES_HOST=postgres
```

It is **not**:

```
localhost
```

Within Docker, services communicate using their service names.

```
FastAPI

connect()

↓

postgres
```

Docker automatically resolves the hostname.

---

## Volume Mapping

```yaml
- .:/app
```

This maps the current project directory into the container.

```
Laptop

project/

↓

Docker Container

/app
```

Any code changes made on your laptop immediately become available inside the container.

This is especially useful during development.

---

## Command

```yaml
command: uvicorn app.api:app --host 0.0.0.0 --port 8000 --reload
```

This command starts the FastAPI server.

Equivalent to running:

```bash
uvicorn app.api:app --host 0.0.0.0 --port 8000 --reload
```

Explanation:

| Option | Description |
|---------|-------------|
| app.api | Python module |
| app | FastAPI application object |
| --host 0.0.0.0 | Allow external access |
| --port 8000 | Listen on port 8000 |
| --reload | Restart automatically when code changes |

---

# Named Volumes

At the bottom of the compose file:

```yaml
volumes:

  postgres_data:

  ollama:
```

Docker creates two persistent volumes.

| Volume | Purpose |
|---------|----------|
| postgres_data | Database storage |
| ollama | Stores downloaded LLM models |

---

# Understanding the Dockerfile

The Dockerfile explains **how to build the FastAPI container**.

```dockerfile
FROM python:3.12

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["uvicorn","api:app","--host","0.0.0.0","--port","8000"]
```

---

## Step 1

```dockerfile
FROM python:3.12
```

This is the base image.

Docker downloads an official image that already contains:

- Linux
- Python 3.12
- Standard Python tools

Everything else is built on top of this image.

---

## Step 2

```dockerfile
WORKDIR /app
```

Sets the working directory inside the container.

Equivalent to:

```bash
cd /app
```

Every subsequent command executes from this directory.

---

## Step 3

```dockerfile
COPY . .
```

Copies the entire project into the container.

```
Your Computer

project/
│
├── api.py
├── requirements.txt
└── app/

↓

Docker Container

/app
│
├── api.py
├── requirements.txt
└── app/
```

---

## Step 4

```dockerfile
RUN pip install -r requirements.txt
```

Installs all Python dependencies required by the application.

Examples include:

- FastAPI
- Uvicorn
- SQLAlchemy
- psycopg
- LangChain
- Other project libraries

This step happens while the image is being built.

---

## Step 5

```dockerfile
CMD ["uvicorn","api:app","--host","0.0.0.0","--port","8000"]
```

This is the command executed when the container starts.

Equivalent to:

```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

Meaning:

- Start the Uvicorn web server.
- Load the FastAPI application named `app` from `api.py`.
- Listen on all network interfaces.
- Use port 8000.

---

# Docker Build vs Docker Run

These are two different phases.

## Build

Creates the Docker image.

```
Dockerfile
      │
      ▼
docker build
      │
      ▼
Docker Image
```

---

## Run

Creates a running container from the image.

```
Docker Image
      │
      ▼
docker run
      │
      ▼
Running Container
```

One image can be used to create many containers.

---

# Complete Application Flow

```
docker compose up
        │
        ▼
Docker builds FastAPI image
        │
        ▼
Starts PostgreSQL
        │
        ▼
Starts Ollama
        │
        ▼
Starts FastAPI
        │
        ▼
Application available at:

http://localhost:8000
```

---

# Summary

This Docker setup provides:

- A PostgreSQL database with pgvector support
- An Ollama server hosting the language model
- A FastAPI application exposing REST APIs
- Persistent storage for both database and models
- Automatic networking between services
- Simple startup using a single command:

```bash
docker compose up
```

With Docker Compose, the entire RAG application stack can be started, stopped, and shared consistently across development, testing, and production environments.