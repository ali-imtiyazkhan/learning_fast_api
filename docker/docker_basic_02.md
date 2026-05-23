# 🐳 Dockerfile — Build Your Own Image

A `Dockerfile` is a text file with step-by-step instructions to build a Docker image of your app.

---

## 📄 Dockerfile for FastAPI (with explanation)

```dockerfile
# ─────────────────────────────────────────
# STEP 1 — Base Image
# Start from an official Python image
# "slim" = smaller size, no unnecessary tools
# ─────────────────────────────────────────
FROM python:3.11-slim

# ─────────────────────────────────────────
# STEP 2 — Set Working Directory
# All future commands run inside /app
# Like doing: cd /app inside the container
# ─────────────────────────────────────────
WORKDIR /app

# ─────────────────────────────────────────
# STEP 3 — Copy requirements first
# Why first? Docker caches layers.
# If requirements didn't change, it skips
# reinstalling — makes builds faster!
# ─────────────────────────────────────────
COPY requirements.txt .

# ─────────────────────────────────────────
# STEP 4 — Install Python packages
# --no-cache-dir = don't store pip cache
# keeps the image smaller
# ─────────────────────────────────────────
RUN pip install --no-cache-dir -r requirements.txt

# ─────────────────────────────────────────
# STEP 5 — Copy all project files
# Copies everything from your folder
# into the /app folder inside the container
# ─────────────────────────────────────────
COPY . .

# ─────────────────────────────────────────
# STEP 6 — Expose Port
# Tells Docker this app uses port 8000
# (This is documentation — doesn't publish it)
# ─────────────────────────────────────────
EXPOSE 8000

# ─────────────────────────────────────────
# STEP 7 — Start Command
# The command that runs when container starts
# uvicorn = the server that runs FastAPI
# --host 0.0.0.0 = accept traffic from outside
# ─────────────────────────────────────────
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 🔨 Build & Run Commands

```bash
# Build image from Dockerfile in current folder
# -t = tag/name for the image
# . = look for Dockerfile in current directory
docker build -t fastapi-app .

# Build with a specific Dockerfile path
docker build -t fastapi-app -f docker/Dockerfile .

# Run the image as a container
docker run -d -p 8000:8000 --name fastapi-app fastapi-app

# Now visit: http://localhost:8000/docs
```

---

## 🧠 Layer Caching (Important Concept!)

```
Each line in Dockerfile = one "layer"
Docker caches each layer separately.
If a layer hasn't changed → Docker reuses it (fast!)
If a layer changed → Docker rebuilds it + everything after it

That's why we COPY requirements.txt BEFORE COPY . .
requirements.txt rarely changes → cached
Your code changes often → always rebuilt
```

---

## 📝 Common Dockerfile Instructions

| Instruction | What it does |
|-------------|-------------|
| `FROM` | Set the base image to start from |
| `WORKDIR` | Set the working directory inside container |
| `COPY` | Copy files from your machine into container |
| `RUN` | Run a shell command during build |
| `ENV` | Set environment variables |
| `EXPOSE` | Document which port the app uses |
| `CMD` | Default command to run when container starts |
| `ENTRYPOINT` | Like CMD but cannot be overridden |

---

## ⚙️ ENV Variables in Dockerfile

```dockerfile
# Set a default env variable
ENV DATABASE_URL=sqlite:///./app.db
ENV DEBUG=true

# Better: pass at runtime (don't hardcode secrets!)
docker run -e DATABASE_URL=postgresql://... fastapi-app
```

---

## 📂 .dockerignore (Always Create This!)

Create a `.dockerignore` file to prevent copying unnecessary files:

```
__pycache__/
*.pyc
*.pyo
.env
.git
.gitignore
*.sqlite
node_modules/
venv/
```

This keeps your image small and secure (no `.env` secrets inside image!).