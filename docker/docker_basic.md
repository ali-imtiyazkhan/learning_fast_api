# 🐳 Docker Basics — Core Commands

Docker lets you package your app into a "container" that runs the same on any machine.

---

## 🔑 Key Concepts

```
Image   → A blueprint/template (like a class in Python)
Container → A running instance of an image (like an object)
Registry → A place to store images (Docker Hub)
```

---

## ✅ Check Docker is Installed

```bash
docker --version
docker info
```

---

## 📦 Image Commands

```bash
# Pull an image from Docker Hub
docker pull python:3.11

# List all images on your machine
docker images

# Remove an image
docker rmi python:3.11

# Search for images on Docker Hub
docker search fastapi
```

---

## 🚀 Container Commands

```bash
# Run a container from an image
docker run python:3.11

# Run with a name
docker run --name my-app python:3.11

# Run in background (detached mode)
docker run -d --name my-app python:3.11

# Run with port mapping (host:container)
docker run -d -p 8000:8000 --name my-app python:3.11

# Run interactively (enter the container shell)
docker run -it python:3.11 bash
```

---

## 📋 Managing Containers

```bash
# List running containers
docker ps

# List ALL containers (including stopped)
docker ps -a

# Stop a running container
docker stop my-app

# Start a stopped container
docker start my-app

# Restart a container
docker restart my-app

# Remove a container
docker rm my-app

# Remove a running container (force)
docker rm -f my-app
```

---

## 🔍 Inspect & Debug

```bash
# See logs of a container
docker logs my-app

# Follow logs in real time
docker logs -f my-app

# Enter a running container's shell
docker exec -it my-app bash

# See container details (IP, config, etc.)
docker inspect my-app

# See resource usage (CPU, RAM)
docker stats
```

---

## 🧹 Cleanup Commands

```bash
# Remove all stopped containers
docker container prune

# Remove all unused images
docker image prune

# Remove EVERYTHING unused (containers, images, networks)
docker system prune

# Nuclear option — removes absolutely everything
docker system prune -a --volumes
```

---

## 💡 Quick Mental Model

```
docker pull   → Download image
docker build  → Create image from Dockerfile
docker run    → Create + start a container
docker stop   → Pause a container
docker rm     → Delete a container
docker rmi    → Delete an image
```