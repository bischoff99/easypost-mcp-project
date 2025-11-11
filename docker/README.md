# Docker Configuration

This directory contains Docker Compose configurations for the EasyPost MCP project.

## Files

- `docker-compose.yml` - Development environment
- `docker-compose.prod.yml` - Production environment
- `nginx-local.conf` - Nginx configuration for local development

## Dockerfiles

Each service has its own Dockerfiles:

- `backend/Dockerfile` - Development build
- `backend/Dockerfile.prod` - Production build (multi-stage, optimized)
- `frontend/Dockerfile` - Development build
- `frontend/Dockerfile.prod` - Production build (multi-stage, nginx)

## Usage

### Development

Start all services:
```bash
docker compose -f docker/docker-compose.yml up
```

Start in detached mode:
```bash
docker compose -f docker/docker-compose.yml up -d
```

View logs:
```bash
docker compose -f docker/docker-compose.yml logs -f
```

Stop services:
```bash
docker compose -f docker/docker-compose.yml down
```

### Production

Start production services:
```bash
docker compose -f docker/docker-compose.prod.yml --env-file .env.production up -d
```

View logs:
```bash
docker compose -f docker/docker-compose.prod.yml logs -f
```

Stop services:
```bash
docker compose -f docker/docker-compose.prod.yml down
```

## Build

Build all images:
```bash
docker compose -f docker/docker-compose.yml build
```

Build specific service:
```bash
docker compose -f docker/docker-compose.yml build backend
docker compose -f docker/docker-compose.yml build frontend
```

## Makefile Commands

The project Makefile provides convenient shortcuts:

- `make prod-docker` - Start production with Docker
- `make build-docker` - Build Docker images

See `Makefile` for all available commands.

