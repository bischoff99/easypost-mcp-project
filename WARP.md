# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

**EasyPost MCP** - Production-ready shipping integration combining EasyPost API with MCP server capabilities, FastAPI backend, and React frontend. Optimized for M3 Max hardware (16 cores, 128GB RAM).

**Stack:** FastAPI (Python 3.14) + React (Vite) + PostgreSQL + FastMCP

## Essential Development Commands

### Development Servers
```bash
# Start both backend and frontend (recommended)
make dev

# Start individually
make backend    # Uvicorn on :8000
make frontend   # Vite dev server on :5173
```

### Testing
```bash
# All tests with 16 parallel workers (M3 Max optimized)
make test

# Fast tests (changed files only)
make test-fast

# Coverage report (45% minimum required)
make test-cov

# Run specific test file
cd backend && ./venv/bin/pytest tests/unit/test_file.py -v

# Run specific test function
cd backend && ./venv/bin/pytest tests/unit/test_file.py::test_function_name -v

# Run integration tests (real EasyPost API calls)
cd backend && ./venv/bin/pytest tests/integration/ -v -m integration
```

### Code Quality
```bash
# Auto-format Python and JavaScript
make format

# Run linters
make lint

# Full quality check (lint + test)
make check
```

### Database Operations
```bash
# Run migrations
cd backend && ./venv/bin/alembic upgrade head

# Create new migration
cd backend && ./venv/bin/alembic revision --autogenerate -m "description"

# Reset database (downgrade + upgrade)
make db-reset
```

### Installation
```bash
# Install all dependencies (both frontend and backend)
make install

# Backend only
cd backend && pip install -r requirements.txt

# Frontend only
cd frontend && npm install
```

## Architecture

### Backend Structure (`backend/src/`)
```
server.py           - FastAPI HTTP server with all REST endpoints
mcp/__init__.py     - FastMCP server initialization
├── tools.py        - MCP tools (create_shipment, track_shipment, etc.)
├── resources.py    - MCP resources
└── prompts.py      - MCP prompts

services/
├── easypost_service.py   - EasyPost API wrapper (async, 32 workers)
├── database_service.py   - PostgreSQL CRUD operations
├── webhook_service.py    - Webhook handling
├── sync_service.py       - Data synchronization
└── smart_customs.py      - Customs data handling

models/               - SQLAlchemy ORM models (9 tables)
routers/              - FastAPI route handlers
database.py           - Dual-pool database configuration
lifespan.py           - App startup/shutdown lifecycle
```

### Database Architecture (Dual-Pool Strategy)

**Pool 1 - SQLAlchemy ORM** (50 connections: 20 base + 30 overflow)
- **Use for:** CRUD operations, single record queries, type-safe operations
- **Access via:** `Depends(get_db)` dependency injection
- **Configuration:** `backend/src/database.py`

**Pool 2 - Direct asyncpg** (32 connections)
- **Use for:** Bulk operations (100+ records), analytics, raw SQL
- **Access via:** `app.state.db_pool` in request handlers
- **Configuration:** `backend/src/lifespan.py`

**Total:** 82 connections (under PostgreSQL default limit of 100)

### Frontend Structure (`frontend/src/`)
```
pages/          - React pages/routes
components/     - Reusable UI components (shadcn-ui)
services/       - API client (axios)
stores/         - Zustand state management
hooks/          - Custom React hooks
```

### MCP Integration

The project runs a **single FastAPI server** on port 8000 with:
1. **Regular HTTP endpoints** (`/health`, `/rates`, etc.) - REST API for web frontend
2. **MCP endpoints** (mounted at `/mcp`) - AI tool integration via FastMCP

**Available MCP Tools:**
- `create_shipment` - Create shipment with label
- `track_shipment` - Track by tracking number
- `get_rates` - Compare carrier rates
- `create_bulk_shipments` - Parallel bulk creation (16 workers)
- `batch_track_shipments` - Track multiple packages

**How it works:**
- FastMCP is mounted at `/mcp` in `backend/src/server.py` (line 129)
- Starting the backend automatically starts both HTTP and MCP endpoints
- Access MCP via: `http://localhost:8000/mcp`

## Key Technical Details

### Async Patterns
All I/O operations use async/await. The codebase is optimized with:
- **uvloop** for 2-4x faster async I/O (when available)
- **asyncio.gather** for parallel operations
- **16-32 workers** for bulk operations (M3 Max optimization)

### Error Handling
Standardized response format across all endpoints:
```python
{
  "status": "success" | "error",
  "data": {...},
  "message": "optional message",
  "request_id": "uuid"
}
```

### Performance Expectations (M3 Max)
- Test suite: 4-6 seconds (16 parallel workers)
- Bulk shipment creation (100): 30-40 seconds
- Batch tracking (50): 2-3 seconds
- Analytics queries (1000 shipments): 1-2 seconds

### Code Conventions

**Python:**
- `snake_case` for functions/variables
- `PascalCase` for classes
- `UPPER_SNAKE_CASE` for constants
- Type hints required
- 100 char line length
- Google-style docstrings

**JavaScript:**
- `camelCase` for functions/variables
- `PascalCase` for React components
- ESLint + Prettier configured
- Functional components with hooks

## Critical Files

### Configuration
- `.dev-config.json` - Development configuration (hardware specs, stack detection, workflows)
- `backend/pyproject.toml` - Python project config, ruff settings
- `backend/pytest.ini` - Test configuration (16 workers, coverage 45%)
- `frontend/package.json` - Node dependencies and scripts

### Environment Setup
- `.env.example` - Template for environment variables
- `.env` - Local environment (gitignored, create from example)
- Backend requires: `EASYPOST_API_KEY`, `DATABASE_URL`
- Frontend requires: `VITE_API_URL` (defaults to http://localhost:8000)

### Database Migrations
- `backend/alembic/` - Migration files
- `backend/alembic.ini` - Alembic configuration
- File naming: `YYYYMMDD_HHMM_rev_slug` format
- Auto-formatted with black on creation

## Common Patterns

### Creating a New Endpoint

1. Add model to `backend/src/models/`
2. Create service method in `backend/src/services/`
3. Add route handler in `backend/src/routers/`
4. Register router in `backend/src/server.py`
5. Write tests in `backend/tests/unit/` and `backend/tests/integration/`

### Database Query Patterns

**Use SQLAlchemy ORM for single records:**
```python
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db

async def get_shipment(id: UUID, db: AsyncSession = Depends(get_db)):
    stmt = select(Shipment).options(
        selectinload(Shipment.from_address),
        selectinload(Shipment.to_address)
    ).where(Shipment.id == id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()
```

**Use direct asyncpg for bulk operations:**
```python
from fastapi import Request

async def batch_operation(request: Request, ids: List[UUID]):
    query = "SELECT * FROM shipments WHERE id = ANY($1)"
    results = await request.app.state.db_pool.fetch(query, ids)
    return results
```

### Testing with Mocks

Tests use factories (`backend/tests/factories.py`) to create mock EasyPost objects:
```python
from tests.factories import create_mock_shipment

def test_shipment_creation(mock_easypost_client):
    # Factory creates realistic test data
    shipment = create_mock_shipment()
    assert shipment.tracking_code is not None
```

## Production Deployment

### Docker
```bash
# Build images
make build-docker

# Start with docker-compose
docker-compose -f docker-compose.prod.yml up
```

### Optional: Nginx Reverse Proxy
For production, nginx provides significant performance benefits:
- 20x faster static asset delivery
- Single URL (eliminates CORS)
- Edge rate limiting
- Browser caching

**Setup:**
```bash
bash scripts/setup-nginx-proxy.sh
```

See `docs/guides/PROXY_AND_DATABASE_INTEGRATION.md` for complete architecture details.

## Troubleshooting

### Backend won't start
- Check `EASYPOST_API_KEY` in `.env` (test key format: `EZTK*`)
- Verify `DATABASE_URL` is set (or use mock mode)
- Check port 8000 is available: `lsof -ti:8000 | xargs kill -9`

### Tests failing
- Run `make test-fast` to see specific failures
- Check test database is accessible
- Verify mocks are working: `pytest tests/unit/ -v -m "not integration"`

### Database connection issues
- Verify PostgreSQL is running
- Check connection string format: `postgresql://user:pass@host:port/dbname`
- Test connection: `psql $DATABASE_URL`
- Database features are optional - app will start without it

### Frontend API errors
- Ensure backend is running on :8000
- Check CORS is configured: `settings.CORS_ORIGINS` in `backend/src/utils/config.py`
- Verify API calls use correct endpoint: `http://localhost:8000/endpoint`

## Additional Resources

- **Complete Cursor/AI Setup:** `.cursor/START_HERE.md`
- **Command Reference:** `.cursor/commands/README.md`
- **Current Workflows:** `.cursor/commands/WORKFLOWS-CURRENT.md`
- **Architecture Diagrams:** `ARCHITECTURE_DIAGRAM.md`
- **Database Integration:** `docs/guides/PROXY_AND_DATABASE_INTEGRATION.md`
- **Contributing Guide:** `CONTRIBUTING.md`
- **Security:** `SECURITY.md`

## Notes for AI Agents

- This project is optimized for **M3 Max hardware** - leverage 16 parallel workers for testing
- Always use **async/await** for I/O operations
- Mock EasyPost API in tests to avoid rate limits (see `conftest.py`)
- Coverage minimum is **45%** for backend, **70%** for frontend
- Run `make format` before committing
- Database is **optional** - app gracefully handles missing DATABASE_URL
- **Single server architecture** - MCP is mounted at `/mcp` on the main FastAPI app
