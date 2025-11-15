# Environment Configuration Guide

Complete guide for configuring development and production environments.

## Overview

The EasyPost MCP project uses environment-specific configuration files:

- **Development**: `.env.development` or `.env` (local overrides)
- **Production**: `.env.production` or `.env` (local overrides)

## Configuration Priority

Configuration files are loaded in this order (later files override earlier ones):

1. `.env.production` or `.env.development` (environment-specific)
2. `.env` (local overrides)
3. Project root `.env` (fallback)

## Quick Start

### Development Setup

1. Copy example file:

   ```bash
   cd /Users/andrejs/Projects/personal/easypost-mcp-project
   cp .env.example .env
   ```

2. Edit `.env` with your development values:

   ```bash
   # Use test API key for development
   EASYPOST_API_KEY=your_test_key_here
   ENVIRONMENT=development
   DEBUG=true
   ```

3. Start development:
   ```bash
   /ep-dev
   # or
   make dev
   ```

### Production Setup

1. Copy production template:

   ```bash
   cd /Users/andrejs/Projects/personal/easypost-mcp-project
   cp .env.production .env
   ```

2. Edit `.env` with production values:

   ```bash
   EASYPOST_API_KEY=your_production_key_here
   ENVIRONMENT=production
   DEBUG=false
   DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/db
   ```

3. Deploy:
   ```bash
   make prod
   # or
   docker-compose -f deploy/docker-compose.prod.yml up -d
   ```

## Backend Configuration

### Required Variables

- `EASYPOST_API_KEY` - EasyPost API key (required)

### Optional Variables

- `DATABASE_URL` - PostgreSQL connection string (optional, disables DB features if not set)
- `ENVIRONMENT` - `development` or `production` (default: `development`)
- `DEBUG` - Enable debug mode (default: `false`)
- `MCP_PORT` - Server port (default: `8000`)
- `MCP_LOG_LEVEL` - Logging level (default: `INFO`)
- `CORS_ORIGINS` - Comma-separated allowed origins
- `MAX_BULK_CONCURRENCY` - Max parallel operations (default: `16`)

### Database Pool Settings

For personal use (defaults are optimized):

```bash
DATABASE_POOL_SIZE=10          # Base connections per worker
DATABASE_MAX_OVERFLOW=5        # Additional connections
DATABASE_POOL_RECYCLE=1800     # Recycle after 30 minutes
DATABASE_POOL_TIMEOUT=10       # Wait 10s for connection
DATABASE_COMMAND_TIMEOUT=60    # Query timeout 60s
DATABASE_CONNECT_TIMEOUT=10    # Connection timeout 10s
DATABASE_STATEMENT_TIMEOUT_MS=15000  # Statement timeout 15s
```

## Environment-Specific Settings

### Development

- **API Key**: Use test key (`EASYPOST_TEST_KEY`)
- **Database**: Local PostgreSQL or empty (DB features disabled)
- **CORS**: Allow all localhost origins
- **Debug**: Enabled (`DEBUG=true`)
- **Log Level**: `DEBUG`
- **Hot Reload**: Enabled

### Production

- **API Key**: Use production key (`EASYPOST_API_KEY`)
- **Database**: Production PostgreSQL URL
- **CORS**: Restricted to your domain
- **Debug**: Disabled (`DEBUG=false`)
- **Log Level**: `INFO`
- **Hot Reload**: Disabled
- **Workers**: 16 (M3 Max optimized)

## Docker Configuration

Production Docker Compose uses environment variables:

```bash
# Set in shell or .env file
export EASYPOST_API_KEY=your_key
export POSTGRES_PASSWORD=your_password
export DOMAIN=yourdomain.com

# Start production stack
docker-compose -f deploy/docker-compose.prod.yml up -d
```

## Security Best Practices

1. **Never commit `.env` files** - They're in `.gitignore`
2. **Use `.env.example`** - Template files are safe to commit
3. **Store secrets securely** - Use macOS Keychain or environment variables
4. **Rotate keys regularly** - Update API keys periodically
5. **Use test keys for development** - Never use production keys locally

## macOS Keychain Integration

Store secrets in Keychain for automatic loading:

```bash
# Store API key
security add-generic-password \
  -a "easypost" \
  -s "easypost-api-key" \
  -w "your_key_here"

# Load in .envrc
export EASYPOST_API_KEY=$(security find-generic-password -s "easypost-api-key" -w 2>/dev/null)
```

## Troubleshooting

### Backend won't start

**Error**: `EASYPOST_API_KEY is required`

**Solution**:

```bash
# Check if .env exists
ls config/.env

# Create from example
cp config/.env.example config/.env

# Edit with your key
nano config/.env
```

### Database connection fails

**Error**: `Database not configured`

**Solution**:

- Development: Leave `DATABASE_URL` empty (DB features disabled)
- Production: Set correct `DATABASE_URL` in `.env`

### CORS errors in browser/clients

**Error**: `CORS policy blocked`

**Solution**:

- Development: Add the requesting origin (if any) to `CORS_ORIGINS`
- Production: Set `CORS_ORIGINS` to trusted domains (or leave empty for MCP-only)

### Environment not detected

**Error**: Wrong environment loaded

**Solution**:

```bash
# Explicitly set environment
export ENVIRONMENT=production

# Or in .env
echo "ENVIRONMENT=production" >> config/.env
```

## Related Files

- `config/.env.example` - Backend configuration template
- `config/.env.development` - Development defaults
- `config/.env.production` - Production defaults
- `.envrc` - direnv configuration (auto-loads .env)
- `deploy/docker-compose.prod.yml` - Production Docker config

## Quick Reference

```bash
# Development
cp config/.env.example config/.env
# Edit .env with test key
/ep-dev

# Production
cp config/.env.production config/.env
# Edit .env with production key
make prod
```
