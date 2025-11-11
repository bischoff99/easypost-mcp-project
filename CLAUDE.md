# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

EasyPost MCP is a production-ready shipping integration with:
- **Backend**: FastAPI + FastMCP server for EasyPost API integration
- **Frontend**: React 19 + Vite 7.2 + TailwindCSS 4
- **Database**: PostgreSQL with dual-pool strategy (SQLAlchemy ORM + asyncpg direct)
- **MCP Tools**: AI agent tools for shipment creation, tracking, and rate comparison

## Development Commands

### Quick Start
```bash
# Start both servers
make dev

# Backend only
cd apps/backend && source venv/bin/activate && uvicorn src.server:app --reload

# Frontend only
cd apps/frontend && pnpm run dev
```

### Testing
```bash
# All tests (16 parallel workers for backend, vitest for frontend)
make test

# Fast tests (changed files only)
make test-fast

# Coverage report
make test-cov

# Run single backend test
cd apps/backend && pytest tests/path/to/test_file.py::test_function_name -v

# Run single frontend test
cd apps/frontend && npm test -- src/path/to/test.test.jsx
```

### Code Quality
```bash
# Lint
make lint

# Auto-format (black + ruff for Python, prettier for JS)
make format

# Full check (lint + test)
make check
```

### Database
```bash
# Reset database
make db-reset

# Create migration
cd apps/backend && alembic revision --autogenerate -m "description"

# Apply migrations
make db-upgrade
```

### Production
```bash
# Build production bundles
make build

# Run production locally
make prod

# Run production with Docker
make prod-docker
```

## Architecture

### Backend Structure
```
apps/backend/src/
├── server.py           # FastAPI app with MCP integration
├── routers/            # API endpoints (shipments, tracking, analytics, webhooks)
├── services/           # Business logic (easypost_service, database_service)
├── models/             # Pydantic request/response & SQLAlchemy ORM models
├── mcp_server/         # FastMCP tools, prompts, and resources
│   ├── tools/          # MCP tools for AI agents
│   ├── prompts/        # Prompt templates
│   └── resources/      # Resource providers
├── database.py         # SQLAlchemy setup & session management
├── lifespan.py         # App startup/shutdown lifecycle
└── utils/              # Config, monitoring, helpers
```

### Frontend Structure
```
apps/frontend/src/
├── App.jsx             # Main app with routing
├── pages/              # Page components (Dashboard, Shipments, Analytics, etc.)
├── components/         # Reusable UI components
│   ├── layout/         # Header, Sidebar
│   ├── shipments/      # Shipment-related components
│   ├── analytics/      # Charts and visualizations
│   └── ui/             # Shadcn-style UI primitives
├── services/           # API client (axios with retry)
└── tests/              # Unit and E2E tests
```

### Database Dual-Pool Strategy

**When to use each pool:**

1. **SQLAlchemy ORM Pool** (`Depends(get_db)`):
   - Single CRUD operations
   - Type-safe queries with relationships
   - Pydantic serialization
   - Example: `async def get_shipment(id: UUID, db: AsyncSession = Depends(get_db))`

2. **asyncpg Direct Pool** (`request.app.state.db_pool`):
   - Bulk operations (100+ records)
   - Analytics aggregations
   - Raw SQL for performance
   - Parallel processing
   - Example: `await pool.fetch("SELECT * FROM shipments WHERE ...")`

3. **DatabaseService** (recommended abstraction):
   - Business logic layer wrapping SQLAlchemy
   - Consistent error handling
   - Example: `service = DatabaseService(db); await service.create_shipment(data)`

### MCP Tools Architecture

MCP (Model Context Protocol) tools are designed for AI agents to interact with the EasyPost API:

- **Tools** (`mcp_server/tools/`): Async functions decorated with `@mcp.tool()`
  - `shipment_tools.py`: Create, buy, void shipments
  - `rate_tools.py`: Get and compare rates
  - `tracking_tools.py`: Track shipments
  - `bulk_tools.py`: Batch operations with parallel processing

- **Resources** (`mcp_server/resources/`): Dynamic data providers for context
  - Statistics, recent shipments, carrier info

- **Prompts** (`mcp_server/prompts/`): Reusable prompt templates
  - Shipping workflows, cost optimization, tracking help

## Key Technologies & Patterns

### Backend

**FastAPI Patterns:**
- Async/await for all I/O operations
- Pydantic v2 for validation
- Dependency injection with `Depends()`
- Early returns for error handling
- Structured logging with context

**Database Patterns:**
- SQLAlchemy 2.0 async style: `select(Model).where()`
- Connection pooling: 50 (SQLAlchemy) + 32 (asyncpg) = 82 total
- Alembic migrations in `apps/backend/alembic/`

**MCP Patterns:**
- FastMCP for tool registration
- Return `{"status": "success/error", "data": ..., "message": "..."}` format
- Parallel processing with `asyncio.gather()` for batch operations
- Structured error responses for AI consumption

**Testing:**
- pytest with 16 parallel workers (`-n 16`)
- Mock EasyPost API calls
- AAA pattern (Arrange, Act, Assert)
- Coverage target: 40%+ (see pytest.ini)

### Frontend

**React Patterns:**
- Functional components with hooks
- React Query for server state
- Zustand for client state
- React Router v7 for navigation
- Error boundaries for graceful error handling

**UI Components:**
- Radix UI primitives + TailwindCSS 4
- Custom components in `components/ui/`
- Framer Motion for animations
- Recharts for analytics

**API Integration:**
- Axios with automatic retry (3 attempts, exponential backoff)
- API client in `services/api.js`
- Error handling with toast notifications

**Testing:**
- Vitest with React Testing Library
- E2E tests with Puppeteer (see `src/tests/e2e/`)

## Important Configuration Files

- **Backend**:
  - `pyproject.toml`: Ruff, Black, mypy configuration
  - `pytest.ini`: Test configuration with 16 parallel workers
  - `requirements.in`: Production dependencies (compile with `pip-compile`)
  - `.env`: Environment variables (EASYPOST_API_KEY, DATABASE_URL)

- **Frontend**:
  - `vite.config.js`: Build optimizations, proxy, code splitting
  - `package.json`: Scripts and dependencies
  - `tailwind.config.js`: TailwindCSS configuration

- **Root**:
  - `Makefile`: Quick development commands
  - `docker-compose.prod.yml`: Production deployment with PostgreSQL
  - `.cursor/rules/`: Comprehensive coding standards (see 00-INDEX.mdc)

## M3 Max Optimizations

This project is optimized for Apple Silicon M3 Max (16 cores):

- **Backend**: 16 pytest workers, uvloop for async I/O, 82 DB connections
- **Frontend**: SWC transpiler, 20 parallel file operations, esbuild minification
- **PostgreSQL**: Tuned for 16GB RAM, 4 CPU cores allocated
- **Uvicorn**: 16 worker processes in production

## Common Workflows

### Adding a New API Endpoint

1. Create route in `apps/backend/src/routers/`
2. Define Pydantic request/response models in `apps/backend/src/models/requests.py`
3. Implement business logic in service layer (`services/`)
4. Add tests in `apps/backend/tests/`
5. Update frontend API client in `apps/frontend/src/services/api.js`

### Adding a New MCP Tool

1. Create tool function in `apps/backend/src/mcp_server/tools/`
2. Decorate with `@mcp.tool()` and add comprehensive docstring
3. Register in `apps/backend/src/mcp_server/tools/__init__.py`
4. Add tests with 100% coverage requirement
5. Document in `docs/guides/MCP_TOOLS_USAGE.md`

### Adding Database Models

1. Create SQLAlchemy model in `apps/backend/src/models/`
2. Export from `apps/backend/src/models/__init__.py`
3. Generate migration: `cd apps/backend && alembic revision --autogenerate -m "add model"`
4. Review and edit migration in `apps/backend/alembic/versions/`
5. Apply: `alembic upgrade head`

## Coding Standards

**Critical rules** (see `.cursor/rules/` for comprehensive details):

1. **Type Safety**: Type hints required for all Python functions; avoid `any` in JavaScript
2. **Error Handling**: Raise errors explicitly, never silently ignore failures
3. **Async Operations**: Use async/await for all I/O operations
4. **Testing**: AAA pattern, mock external APIs, parametrized tests
5. **Security**: No hardcoded secrets, parameterized queries, input validation

**Import Sorting** (handled by Ruff):
- Future imports
- Standard library
- Third-party (fastapi, pydantic, sqlalchemy, easypost)
- First-party (src.*)
- Local folder

**Commit Format**:
```
type(scope): description

Examples:
feat: add bulk shipment creation endpoint
fix: resolve tracking number validation bug
docs: update MCP tools documentation
refactor: extract address validation logic
test: add tests for rate calculation
```

## Running as MCP Server

The backend can run as a standalone MCP server for AI agents:

```bash
# In Claude Desktop config (claude_desktop_config.json):
{
  "mcpServers": {
    "easypost": {
      "command": "/path/to/backend/venv/bin/python",
      "args": ["-m", "src.mcp_server"],
      "env": {
        "EASYPOST_API_KEY": "your_key_here",
        "DATABASE_URL": "postgresql+asyncpg://..."
      }
    }
  }
}
```

## Documentation

- **Project Guides**: `docs/guides/`
  - `QUICK_REFERENCE.md`: Code templates and patterns
  - `PROXY_AND_DATABASE_INTEGRATION.md`: Architecture deep dive
  - `MCP_TOOLS_USAGE.md`: MCP tool documentation
  - `BULK_RATES_DATA.md`: Bulk operations guide

- **Review Reports**: `docs/reviews/`
  - Comprehensive project reviews and analysis

- **Cursor Rules**: `.cursor/rules/`
  - `00-INDEX.mdc`: Complete rules index
  - `01-fastapi-python.mdc`: Backend best practices
  - `02-react-vite-frontend.mdc`: Frontend best practices
  - `03-testing-best-practices.mdc`: Testing strategy
  - `04-mcp-development.mdc`: MCP tool development
  - `05-m3-max-optimizations.mdc`: Performance optimization

## Environment Setup

**Backend**:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Add EASYPOST_API_KEY
alembic upgrade head  # Initialize database
```

**Frontend**:
```bash
cd frontend
npm install
```

**Database** (using Docker):
```bash
docker-compose -f docker-compose.prod.yml up postgres -d
```

## URLs

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## Troubleshooting

**Backend issues:**
- Check logs: Backend logs to stdout with structured logging
- Database connection: Verify `DATABASE_URL` in `.env`
- EasyPost API: Ensure `EASYPOST_API_KEY` is valid (test/production)

**Frontend issues:**
- Check console for errors
- Verify backend is running on port 8000
- Clear Vite cache: `rm -rf frontend/node_modules/.vite`

**Database issues:**
- Reset: `make db-reset`
- Check migrations: `cd backend && alembic current`
- View logs: `docker-compose -f docker-compose.prod.yml logs postgres`

**Test failures:**
- Run serially for debugging: `pytest tests/file.py -v` (without `-n 16`)
- Check mocks: Ensure EasyPost API calls are mocked
- View coverage: `make test-cov` then open `backend/htmlcov/index.html`
