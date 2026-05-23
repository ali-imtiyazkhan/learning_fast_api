# 🐳 Docker Complete Workflow & Cheatsheet

The full journey from writing code → building image → running container → pushing to registry.

---

## 🗺️ Docker Workflow (Step by Step)

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│   1. Write Code                                     │
│      └── main.py, requirements.txt, etc.            │
│                                                     │
│   2. Write Dockerfile                               │
│      └── Instructions to build the image            │
│                                                     │
│   3. Build Image                                    │
│      └── docker build -t my-app .                   │
│                                                     │
│   4. Run Container                                  │
│      └── docker run -p 8000:8000 my-app             │
│                                                     │
│   5. Test                                           │
│      └── http://localhost:8000/docs                 │
│                                                     │
│   6. Push to Docker Hub (optional)                  │
│      └── docker push username/my-app                │
│                                                     │
│   7. Pull & Run Anywhere                            │
│      └── docker pull username/my-app                │
│      └── docker run username/my-app                 │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 🚀 Full FastAPI Docker Workflow

### Step 1 — Project Files Ready

```
fastapi_project/
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── requirements.txt
└── main.py
```

### Step 2 — Build the Image

```bash
# Go into your project folder
cd fastapi_project

# Build image, tag it as "fastapi-app"
docker build -t fastapi-app .

# Verify image was created
docker images
```

### Step 3 — Run the Container

```bash
# Run with port mapping
docker run -d -p 8000:8000 --name fastapi-app fastapi-app

# Check it's running
docker ps

# Test it
curl http://localhost:8000
# Or open: http://localhost:8000/docs
```

### Step 4 — Debug if Something Goes Wrong

```bash
# Check logs
docker logs fastapi-app

# Enter the container shell
docker exec -it fastapi-app bash

# Inside container — check files
ls /app
cat /app/main.py

# Exit container
exit
```

### Step 5 — Stop & Clean Up

```bash
docker stop fastapi-app
docker rm fastapi-app
docker rmi fastapi-app
```

---

## 🐙 Docker Hub — Push & Pull Images

```bash
# Login to Docker Hub
docker login

# Tag your image with your username
# Format: username/image-name:version
docker tag fastapi-app imtiyaz/fastapi-app:v1.0

# Push to Docker Hub
docker push imtiyaz/fastapi-app:v1.0

# Anyone can now pull and run it
docker pull imtiyaz/fastapi-app:v1.0
docker run -p 8000:8000 imtiyaz/fastapi-app:v1.0
```

---

## ⚡ Docker Compose Workflow (Recommended)

```bash
# Start everything (builds automatically if needed)
docker compose up -d

# Rebuild after code changes
docker compose up -d --build

# See all running services
docker compose ps

# Check logs
docker compose logs -f

# Stop everything
docker compose down

# Stop and wipe database too
docker compose down -v
```

---

## 🧠 Mental Model — Image vs Container

```
Image = Recipe (inactive, just instructions)
Container = Cooked dish (active, running)

One image → can run many containers
docker run my-app          → container 1
docker run my-app          → container 2
docker run my-app          → container 3
```

---

## 📋 Master Cheatsheet

### Images
```bash
docker build -t name .          # Build image
docker images                   # List images
docker rmi name                 # Delete image
docker pull name                # Download image
docker push name                # Upload image
docker tag old new              # Rename/tag image
```

### Containers
```bash
docker run -d -p 8000:8000 name     # Run detached + port
docker run -it name bash            # Run interactively
docker ps                           # List running
docker ps -a                        # List all
docker stop name                    # Stop
docker start name                   # Start
docker restart name                 # Restart
docker rm name                      # Delete
docker rm -f name                   # Force delete
docker logs name                    # View logs
docker logs -f name                 # Follow logs
docker exec -it name bash           # Enter shell
docker inspect name                 # Full details
docker stats                        # Resource usage
```

### Compose
```bash
docker compose up -d                # Start all
docker compose up -d --build        # Rebuild + start
docker compose down                 # Stop all
docker compose down -v              # Stop + delete volumes
docker compose ps                   # List services
docker compose logs -f              # Follow all logs
docker compose logs -f app          # Follow one service
docker compose exec app bash        # Enter service shell
docker compose restart app          # Restart one service
```

### Volumes
```bash
docker volume create name           # Create
docker volume ls                    # List
docker volume rm name               # Delete
docker volume prune                 # Delete unused
```

### Networks
```bash
docker network create name          # Create
docker network ls                   # List
docker network rm name              # Delete
docker network inspect name         # Inspect
```

### Cleanup
```bash
docker system prune                 # Remove unused stuff
docker system prune -a --volumes    # Remove EVERYTHING
docker container prune              # Remove stopped containers
docker image prune                  # Remove dangling images
```

---

## 🔥 Most Used Commands (Daily Use)

```bash
docker compose up -d --build    # Start project
docker compose logs -f          # Watch logs
docker compose down             # Stop project
docker exec -it app bash        # Debug inside container
docker system prune             # Clean up disk space
```

---

## 📚 Learning Path

```
Week 1 → docker run, docker ps, docker logs        (01_docker_basics.md)
Week 2 → Write Dockerfiles, docker build            (02_dockerfile.md)
Week 3 → docker-compose.yml, multi-container apps  (03_docker_compose.md)
Week 4 → Volumes, networks, data persistence       (04_volumes_and_networking.md)
Week 5 → Push to Docker Hub, deploy to cloud       (this file ↑)
```