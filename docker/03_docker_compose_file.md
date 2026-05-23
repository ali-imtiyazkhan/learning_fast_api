# 🐳 Docker Compose — Run Multiple Containers Together

Docker Compose lets you define and run **multiple containers** as one service using a single `docker-compose.yml` file.

---

## 🤔 Why Compose?

```
Without Compose:
  docker run -d postgres ...       (long command)
  docker run -d -p 8000:8000 ...  (another long command)
  docker network connect ...       (link them manually)

With Compose:
  docker compose up                (ONE command, done ✅)
```

---

## 📄 docker-compose.yml for FastAPI + PostgreSQL

```yaml
# Version of Docker Compose syntax
version: "3.9"

services:

  # ──────────────────────────────────────
  # SERVICE 1: FastAPI App
  # ──────────────────────────────────────
  app:
    # Build from Dockerfile in current directory
    build: .

    # Name the container
    container_name: fastapi-app

    # Map port 8000 on your machine → port 8000 in container
    ports:
      - "8000:8000"

    # Pass environment variables to the container
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/fastapi_db
      - DEBUG=true

    # Wait for db to be healthy before starting app
    depends_on:
      db:
        condition: service_healthy

    # Mount your code folder into the container
    # Changes in your code reflect instantly (hot reload)
    volumes:
      - .:/app

    # Run with hot reload for development
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload

    # Connect to the shared network
    networks:
      - app-network

  # ──────────────────────────────────────
  # SERVICE 2: PostgreSQL Database
  # ──────────────────────────────────────
  db:
    # Use official PostgreSQL image
    image: postgres:15

    container_name: postgres-db

    # DB credentials
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
      POSTGRES_DB: fastapi_db

    # Save DB data permanently (survives container restart)
    volumes:
      - postgres_data:/var/lib/postgresql/data

    # Expose DB port (optional — only needed to connect via DB tool)
    ports:
      - "5432:5432"

    # Health check — app waits until DB is truly ready
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

    networks:
      - app-network

# ──────────────────────────────────────
# VOLUMES — Persistent Storage
# Data survives even if container is deleted
# ──────────────────────────────────────
volumes:
  postgres_data:

# ──────────────────────────────────────
# NETWORKS — Internal Communication
# Containers on same network can talk to each other
# App uses "db" as the hostname to reach PostgreSQL
# ──────────────────────────────────────
networks:
  app-network:
    driver: bridge
```

---

## ▶️ Docker Compose Commands

```bash
# Start all services (builds if needed)
docker compose up

# Start in background (detached)
docker compose up -d

# Build images before starting
docker compose up --build

# Stop all services
docker compose down

# Stop AND remove volumes (wipes DB data!)
docker compose down -v

# See logs of all services
docker compose logs

# See logs of one service
docker compose logs app
docker compose logs db

# Follow logs in real time
docker compose logs -f app

# See running services
docker compose ps

# Restart one service
docker compose restart app

# Run a command inside a service container
docker compose exec app bash
docker compose exec db psql -U postgres
```

---

## 🧠 Key Concepts

```
services  → Each container you want to run
volumes   → Persistent storage (survives restart/delete)
networks  → Private network so containers talk to each other
depends_on → Start order (db starts before app)
```

---

## 🔗 How Containers Talk to Each Other

```
In docker-compose.yml, service name = hostname

So inside the "app" container:
  Database host = "db"        (not localhost!)
  DATABASE_URL  = postgresql://postgres:password@db:5432/fastapi_db
                                                    ^^
                                               service name
```

---

## 📁 Recommended File Layout

```
fastapi_project/
├── docker-compose.yml     ← Compose config
├── Dockerfile             ← App image instructions
├── .dockerignore          ← Files to exclude
├── .env                   ← Secrets (never commit!)
├── main.py
└── ...
```