# Docker Deployment

Docker configuration for the EasyPost MCP project (personal use).

## Files

- `Dockerfile` - Docker image build configuration
- `docker-compose.yml` - Local development environment

## Usage

### Development

Start services:

```bash
docker compose -f deploy/docker-compose.yml up
```

Start in detached mode:

```bash
docker compose -f deploy/docker-compose.yml up -d
```

View logs:

```bash
docker compose -f deploy/docker-compose.yml logs -f
```

Stop services:

```bash
docker compose -f deploy/docker-compose.yml down
```

### Build

Build Docker image:

```bash
docker compose -f deploy/docker-compose.yml build
```

## Environment Variables

Create a `.env` file with:

```env
EASYPOST_API_KEY=your_api_key_here
```

## Note

This is a personal-use, backend-only project. The Docker setup includes only the backend service. Database persistence has been removed - all data is fetched directly from EasyPost API on-demand.
