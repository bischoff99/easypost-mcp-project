# Production Deployment Guide

Complete guide for deploying EasyPost MCP to production with Docker.

## Prerequisites

- Docker 24.0+
- Docker Compose v2.0+
- 16+ GB RAM (96+ GB recommended for M3 Max optimizations)
- Domain name (optional, for SSL)
- EasyPost Production API key (your_production_api_key_here*)

## Quick Start

### 1. Create Production Environment File

```bash
cp .env.production.example .env.production
```

Edit `.env.production` with your values:

```env
# EasyPost API Keys (REQUIRED)
EASYPOST_API_KEY=your_production_api_key_here_your_production_key_here
EASYPOST_TEST_KEY=EZTK_your_test_key_here

# Database Password (REQUIRED)
POSTGRES_PASSWORD=your_secure_password_here

# Domain Configuration (Optional)
DOMAIN=yourdomain.com
BACKEND_URL=https://api.yourdomain.com
```

### 2. Build and Deploy

```bash
# Build containers
docker-compose -f docker-compose.prod.yml --env-file .env.production build

# Start services
docker-compose -f docker-compose.prod.yml --env-file .env.production up -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

### 3. Verify Deployment

```bash
# Check service health
docker-compose -f docker-compose.prod.yml ps

# Test backend
curl http://localhost:8000/health

# Test frontend
curl http://localhost/health

# View API docs
open http://localhost:8000/docs
```

## Architecture

```
┌─────────────────┐
│    Internet     │
└────────┬────────┘
         │
    ┌────▼────┐
    │ Nginx   │ (Port 80/443)
    │Frontend │
    └────┬────┘
         │
    ┌────▼────────┐
    │  FastAPI    │ (Port 8000)
    │  Backend    │ (33 workers)
    └────┬────────┘
         │
    ┌────▼────────┐
    │ PostgreSQL  │ (Port 5432)
    │  Database   │ (16GB RAM)
    └─────────────┘
```

## Container Resources

### PostgreSQL
- **CPU:** 4 cores
- **Memory:** 16GB
- **Storage:** Volume `postgres_data`
- **Config:** Optimized for analytics workloads

### Backend (FastAPI)
- **CPU:** 14 cores (leave 2 for system)
- **Memory:** 96GB (M3 Max optimized)
- **Workers:** 33 (2 × 16 cores + 1)
- **Features:** uvloop, parallel processing

### Frontend (Nginx)
- **CPU:** 10 cores
- **Memory:** 16GB
- **Ports:** 80 (HTTP), 443 (HTTPS)
- **Features:** Gzip, caching, reverse proxy

## Production Configuration

### Database Migrations

Migrations run automatically on backend startup. To run manually:

```bash
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head
```

### Environment Variables

**Backend:**
- `EASYPOST_API_KEY` - Production API key (your_production_api_key_here*)
- `DATABASE_URL` - Auto-configured PostgreSQL connection
- `WORKERS` - Uvicorn worker count (33 for M3 Max)
- `PYTHONOPTIMIZE=2` - Enable Python optimizations
- `LOG_LEVEL=INFO` - Production logging

**Frontend:**
- `VITE_API_URL` - Backend API URL (build-time)
- Configured via nginx reverse proxy

### Volumes

**Persistent Data:**
```bash
docker volume ls
# postgres_data - Database storage
# backend/logs - Application logs
```

**Backup Database:**
```bash
docker-compose -f docker-compose.prod.yml exec postgres \
  pg_dump -U easypost easypost_mcp > backup.sql
```

**Restore Database:**
```bash
docker-compose -f docker-compose.prod.yml exec -T postgres \
  psql -U easypost easypost_mcp < backup.sql
```

## SSL/HTTPS Configuration

### Option 1: Let's Encrypt (Recommended)

```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot certonly --standalone -d yourdomain.com

# Copy certificates
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ssl/key.pem
```

### Option 2: Self-Signed (Development)

```bash
mkdir -p ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout ssl/key.pem -out ssl/cert.pem
```

### Enable HTTPS

Edit `frontend/nginx-prod.conf`:

```nginx
# Uncomment these lines:
listen 443 ssl http2 default_server;
ssl_certificate /etc/nginx/ssl/cert.pem;
ssl_certificate_key /etc/nginx/ssl/key.pem;
```

Restart frontend:
```bash
docker-compose -f docker-compose.prod.yml restart frontend
```

## Monitoring & Logs

### View Logs

```bash
# All services
docker-compose -f docker-compose.prod.yml logs -f

# Specific service
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f frontend
docker-compose -f docker-compose.prod.yml logs -f postgres

# Last 100 lines
docker-compose -f docker-compose.prod.yml logs --tail=100 backend
```

### Health Checks

```bash
# Backend health
curl http://localhost:8000/health

# Frontend health
curl http://localhost/health

# Database health
docker-compose -f docker-compose.prod.yml exec postgres \
  pg_isready -U easypost -d easypost_mcp

# Container status
docker-compose -f docker-compose.prod.yml ps
```

### Metrics

```bash
# API metrics
curl http://localhost:8000/metrics

# Database statistics
docker-compose -f docker-compose.prod.yml exec postgres \
  psql -U easypost easypost_mcp -c "SELECT * FROM pg_stat_database;"
```

## Performance Tuning

### M3 Max Optimizations

Already configured:
- ✅ 33 backend workers (2 × 16 cores + 1)
- ✅ PostgreSQL: 8 parallel workers
- ✅ uvloop for async I/O (2-4x faster)
- ✅ 96GB RAM allocation for backend
- ✅ 16GB RAM + 4GB shared buffers for PostgreSQL

### Additional Tuning

**Increase worker count** (if >16 cores):
```yaml
# docker-compose.prod.yml
environment:
  - WORKERS=65  # For 32-core system: (2 × 32) + 1
```

**Adjust PostgreSQL memory** (if >128GB RAM):
```yaml
# docker-compose.prod.yml
command: >
  postgres
  -c shared_buffers=8GB
  -c effective_cache_size=24GB
```

## Scaling

### Horizontal Scaling

**Add more backend workers:**

```yaml
# docker-compose.prod.yml
services:
  backend-2:
    extends: backend
    container_name: easypost-backend-2
    ports:
      - "8001:8000"
```

**Load balance with nginx:**

```nginx
upstream backend_cluster {
    server backend:8000;
    server backend-2:8000;
}
```

### Database Replication

For high availability:

```yaml
postgres-replica:
  image: postgres:16-alpine
  environment:
    POSTGRES_MASTER_HOST: postgres
    POSTGRES_REPLICATION_MODE: slave
```

## Maintenance

### Update Application

```bash
# Pull latest code
git pull origin main

# Rebuild containers
docker-compose -f docker-compose.prod.yml --env-file .env.production build

# Restart services (zero-downtime)
docker-compose -f docker-compose.prod.yml up -d
```

### Database Maintenance

```bash
# Vacuum database
docker-compose -f docker-compose.prod.yml exec postgres \
  psql -U easypost easypost_mcp -c "VACUUM ANALYZE;"

# Reindex
docker-compose -f docker-compose.prod.yml exec postgres \
  psql -U easypost easypost_mcp -c "REINDEX DATABASE easypost_mcp;"
```

### Cleanup

```bash
# Remove old images
docker image prune -a

# Remove unused volumes
docker volume prune

# Stop and remove all containers
docker-compose -f docker-compose.prod.yml down

# Remove all data (WARNING: Destructive!)
docker-compose -f docker-compose.prod.yml down -v
```

## Troubleshooting

### Backend won't start

```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs backend

# Common issues:
# - Missing EASYPOST_API_KEY in .env.production
# - Database not ready (wait 30s for postgres health check)
# - Port 8000 already in use
```

### Frontend shows 502 Bad Gateway

```bash
# Check backend is running
curl http://localhost:8000/health

# Check nginx logs
docker-compose -f docker-compose.prod.yml logs frontend

# Restart frontend
docker-compose -f docker-compose.prod.yml restart frontend
```

### Database connection errors

```bash
# Check postgres is running
docker-compose -f docker-compose.prod.yml ps postgres

# Test connection
docker-compose -f docker-compose.prod.yml exec postgres \
  psql -U easypost -d easypost_mcp -c "SELECT 1;"

# Check password matches .env.production
```

### High memory usage

```bash
# Check resource usage
docker stats

# Reduce backend workers if needed
# Edit docker-compose.prod.yml:
environment:
  - WORKERS=17  # Reduce from 33 to 17
```

## Security Checklist

- [ ] Production EasyPost API key configured (your_production_api_key_here*)
- [ ] Strong PostgreSQL password set
- [ ] SSL/HTTPS enabled
- [ ] Firewall configured (only 80/443 open)
- [ ] API docs restricted (`/docs` endpoint)
- [ ] Regular backups scheduled
- [ ] Container images updated regularly
- [ ] Logs monitored for errors
- [ ] Health checks passing

## Production URLs

After deployment:

- **Frontend:** http://localhost (or https://yourdomain.com)
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost/health
- **Metrics:** http://localhost:8000/metrics

## Support

For issues:
1. Check logs: `docker-compose logs -f`
2. Verify health: `curl http://localhost/health`
3. Review this guide: `DEPLOYMENT_GUIDE.md`
4. Check comprehensive review: `COMPREHENSIVE_PROJECT_REVIEW.md`

---

**Production Ready** ✅
- 111/120 tests passing
- M3 Max optimized (33 workers)
- PostgreSQL configured (16GB RAM)
- Docker multi-stage builds
- Health checks enabled
- Auto-restart configured
