# Deployment Guide

## Quick Start with Docker

1. **Copy environment file**:
```bash
cp .env.example .env
```

2. **Add your EasyPost API key** to `.env`:
```
EASYPOST_API_KEY=your_actual_key_here
```

3. **Start services**:
```bash
docker-compose up -d
```

4. **Access the application**:
- Frontend: http://localhost
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Alternative API Docs: http://localhost:8000/redoc

## Development Setup

### Backend
```bash
cd backend
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python src/server.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Production Deployment

### Prerequisites
- Docker 24.0+
- Docker Compose 2.20+
- Valid EasyPost API key

### Environment Variables

#### Backend
- `EASYPOST_API_KEY` - Your EasyPost API key (required)
- `MCP_HOST` - Server host (default: 0.0.0.0)
- `MCP_PORT` - Server port (default: 8000)
- `MCP_LOG_LEVEL` - Logging level (default: INFO)
- `CORS_ORIGINS` - Allowed CORS origins

#### Frontend
- `VITE_API_URL` - Backend API URL

### Health Checks

Both services include health check endpoints:
- Backend: `http://localhost:8000/health`
- Frontend: `http://localhost/health`

### Monitoring

Access application metrics at:
- `http://localhost:8000/metrics`

### Scaling

To scale services:
```bash
docker-compose up -d --scale backend=3
```

### Logs

View logs:
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Stopping Services

```bash
docker-compose down  # Stop and remove containers
docker-compose down -v  # Also remove volumes
```

## CI/CD

GitHub Actions workflows are configured for:
- **Backend CI**: Testing, linting, type checking
- **Frontend CI**: Testing, linting, building
- **Docker Build**: Automated image builds on push

Workflows run on pushes to `master`, `main`, or `develop` branches.

## Troubleshooting

### Backend won't start
- Check `EASYPOST_API_KEY` is set correctly
- Verify port 8000 is not in use: `lsof -i :8000`
- Check logs: `docker-compose logs backend`

### Frontend can't connect to backend
- Ensure backend is healthy: `curl http://localhost:8000/health`
- Check CORS configuration in backend `.env`
- Verify proxy settings in `nginx.conf`

### Docker build fails
- Clear build cache: `docker-compose build --no-cache`
- Check Docker disk space: `docker system df`
- Remove unused images: `docker system prune -a`

## Security Notes

- Never commit `.env` files
- Use secrets management in production
- Enable HTTPS with reverse proxy (nginx, Caddy)
- Keep dependencies updated
- Review security advisories regularly

## Performance Tips

- Use Redis for caching (future enhancement)
- Enable CDN for static assets
- Configure nginx gzip compression (already enabled)
- Monitor with Prometheus/Grafana (future enhancement)
