# 🐳 Docker Volumes & Networking

Two of the most important concepts in Docker — how data is saved and how containers communicate.

---

## 💾 PART 1 — Volumes (Persistent Storage)

By default, **all data inside a container is lost when you delete it**.
Volumes solve this by storing data OUTSIDE the container.

```
Without Volume:
  Container deleted → Database gone 💀

With Volume:
  Container deleted → Data still safe ✅
  New container created → Data restored ✅
```

---

### Types of Storage in Docker

```
1. Volume (recommended)     → Managed by Docker, stored in Docker's folder
2. Bind Mount               → Your actual folder mapped into the container
3. tmpfs Mount              → Stored in RAM only, lost on restart
```

---

### Volume Commands

```bash
# Create a named volume
docker volume create mydata

# List all volumes
docker volume ls

# Inspect a volume (see where it's stored)
docker volume inspect mydata

# Remove a volume
docker volume rm mydata

# Remove all unused volumes
docker volume prune
```

---

### Using Volumes with Containers

```bash
# Named Volume — Docker manages storage location
# -v volume_name:path_inside_container
docker run -d \
  -v postgres_data:/var/lib/postgresql/data \
  --name mydb \
  postgres:15

# Bind Mount — maps YOUR folder into container
# Great for development (code changes reflect instantly!)
# -v /your/local/path:/container/path
docker run -d \
  -v $(pwd):/app \
  -p 8000:8000 \
  --name fastapi-app \
  fastapi-app

# Read-only bind mount (container cannot modify files)
docker run -v $(pwd):/app:ro fastapi-app
```

---

### In docker-compose.yml

```yaml
services:
  app:
    volumes:
      - .:/app                    # Bind mount — your code into container
      - .env:/app/.env            # Mount single file

  db:
    volumes:
      - postgres_data:/var/lib/postgresql/data  # Named volume

volumes:
  postgres_data:   # Declare named volumes here
```

---

## 🌐 PART 2 — Networking

Docker networking controls how containers communicate with each other and the outside world.

---

### Network Types

```
bridge   → Default. Containers on same bridge can talk to each other
host     → Container shares your machine's network (no isolation)
none     → No network at all (fully isolated)
overlay  → Multi-machine networking (used in Docker Swarm)
```

---

### Network Commands

```bash
# List all networks
docker network ls

# Create a custom network
docker network create my-network

# Connect a running container to a network
docker network connect my-network my-container

# Disconnect from a network
docker network disconnect my-network my-container

# Inspect a network (see connected containers)
docker network inspect my-network

# Remove a network
docker network rm my-network
```

---

### Connecting Containers Manually

```bash
# Create a shared network
docker network create app-network

# Run PostgreSQL on that network
docker run -d \
  --name db \
  --network app-network \
  -e POSTGRES_PASSWORD=password \
  postgres:15

# Run FastAPI on the same network
# Now "app" can reach "db" using hostname "db"
docker run -d \
  --name app \
  --network app-network \
  -p 8000:8000 \
  fastapi-app
```

---

### Port Mapping Explained

```
-p 8000:8000
    │     │
    │     └── Port INSIDE the container
    └──────── Port on YOUR machine (host)

-p 5432:5432   → PostgreSQL
-p 8000:8000   → FastAPI
-p 80:80       → Nginx/HTTP
-p 443:443     → HTTPS

Access in browser: http://localhost:8000
```

---

### How DNS Works Inside Docker

```
When containers are on the same network:
  Container name = Hostname

Example:
  Service named "db" → reachable at hostname "db"
  Service named "app" → reachable at hostname "app"

So DATABASE_URL = postgresql://user:pass@db:5432/mydb
                                              ^^
                                     container name as host
```

---

## 🧠 Summary Cheatsheet

```
VOLUMES
─────────────────────────────────────────────
docker volume create name       Create volume
docker volume ls                List volumes
docker volume rm name           Delete volume
-v name:/path                   Use named volume
-v $(pwd):/path                 Bind mount (dev)

NETWORKING
─────────────────────────────────────────────
docker network create name      Create network
docker network ls               List networks
docker network inspect name     Inspect network
--network name                  Attach to network
-p 8000:8000                    Publish port
```