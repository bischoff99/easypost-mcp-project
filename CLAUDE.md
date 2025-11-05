# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

EasyPost MCP (Model Context Protocol) server with FastAPI backend and React frontend for shipping operations. The project integrates with EasyPost's shipping API and PostgreSQL database to provide shipment creation, tracking, rate comparison, and analytics with M3 Max hardware optimizations.

**Stack:**
- Backend: Python 3.10+, FastAPI, FastMCP, EasyPost SDK, PostgreSQL, SQLAlchemy 2.0
- Frontend: React 18, Vite, TanStack Query, Zustand, Tailwind CSS
- Database: PostgreSQL 14+ with asyncpg driver, Alembic migrations
- Testing: pytest (backend), Vitest (frontend)
- Performance: uvloop, parallel processing optimized for 16-core M3 Max

## Development Commands

### Quick Start
```bash
# PostgreSQL setup (required)
# Install PostgreSQL 14+ if not already installed
# macOS: brew install postgresql@14
# Create database
createdb easypost_mcp

# Backend setup
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env to add DATABASE_URL and EASYPOST_API_KEY

# Run database migrations
alembic upgrade head

# Frontend setup
cd frontend
npm install

# Start both servers
make dev                  # or use scripts/start-dev.sh
# Backend: http://localhost:8000
# Frontend: http://localhost:5173
```

### Testing
```bash
# Backend tests (16 parallel workers via pytest.ini)
cd backend && source venv/bin/activate
pytest tests/                           # All tests
pytest tests/unit/                      # Unit tests only
pytest tests/integration/               # Integration tests (live API)
pytest tests/integration/test_bulk_performance.py  # Benchmarks

# Frontend tests
cd frontend
npm test                                # Interactive mode
npm run test:coverage                   # With coverage

# Makefile shortcuts
make test                              # All tests
make test-fast                         # Changed files only with -n auto
make test-cov                          # Coverage reports
```

### Code Quality
```bash
# Backend (uses pyproject.toml config)
cd backend && source venv/bin/activate
ruff check src/ tests/                 # Linting
black src/ tests/                      # Formatting
mypy src/                              # Type checking

# Frontend
cd frontend
npm run lint                           # ESLint
npm run format                         # Prettier

# Makefile shortcuts
make lint                              # Run all linters
make format                            # Auto-format all code
```

### Database Management
```bash
cd backend && source venv/bin/activate

# Migrations
alembic upgrade head                   # Run all migrations
alembic downgrade -1                   # Rollback one migration
alembic current                        # Show current version
alembic history                        # Show migration history
alembic revision -m "description"      # Create new migration

# Database operations
psql easypost_mcp                      # Connect to database
psql easypost_mcp -c "SELECT COUNT(*) FROM shipments;"  # Quick query

# Reset database (careful!)
alembic downgrade base                 # Remove all tables
alembic upgrade head                   # Recreate all tables
```

### Running Individual Components
```bash
# Backend only
cd backend && source venv/bin/activate
uvicorn src.server:app --reload        # Development
uvicorn src.server:app --workers 33    # Production (M3 Max: 2*16+1)

# Frontend only
cd frontend
npm run dev

# MCP server only (for MCP client integration)
cd backend && source venv/bin/activate
python -m src.mcp
```

### Environment Management
```bash
# Development (uses .env.development with test API key EZTK*)
ENVIRONMENT=development uvicorn src.server:app --reload

# Production (uses .env.production with live API key EZAK*)
ENVIRONMENT=production uvicorn src.server:app

# VS Code Tasks available for quick switching:
# Cmd+Shift+P → "Run Task" → "🚀 Dev: Full Stack"
```

## Architecture

### Backend Structure

**FastAPI Server** (`backend/src/server.py`):
- Main HTTP API with analytics, rates, shipments, tracking endpoints
- Uses uvloop for 2-4x async I/O performance
- Rate limiting (10 req/min for most endpoints, 20 for analytics)
- Request ID middleware for tracing
- Parallel analytics processing (16 chunks via asyncio.gather)
- Hybrid data architecture: EasyPost API + PostgreSQL database

**MCP Server** (`backend/src/mcp/`):
- Separate FastMCP server for Claude Desktop integration
- Tools: shipment creation, tracking, rates, bulk operations
- Resources: shipment lists, statistics
- Prompts: shipping optimization, carrier comparison, tracking assistance

**Key Services**:
- `EasyPostService` (`backend/src/services/easypost_service.py`): Async wrapper around EasyPost SDK with ThreadPoolExecutor (32-40 workers on M3 Max)
- `DatabaseService` (`backend/src/services/database_service.py`): Comprehensive CRUD operations for PostgreSQL (548 lines, 9 tables with advanced queries)
- `monitoring.py`: Health checks and metrics tracking
- `config.py`: Environment-based configuration (development/production)

**Data Architecture** (Hybrid Approach):
```
API Request
    ├──> EasyPost API (Primary)
    │    └─ Real-time shipment operations
    │    └─ Rate quotes and label creation
    │
    └──> PostgreSQL Database (Secondary)
         └─ Historical data storage (9 tables)
         └─ Analytics aggregation
         └─ User activity tracking
         └─ Batch operation logs
```

**Database Schema** (9 tables):
- `shipments`: Core shipment data with optimized indexes
- `addresses`: From/to addresses with verification
- `parcels`: Package dimensions and weight
- `customs_infos`: International shipping data
- `shipment_events`: Tracking event timeline
- `analytics_summaries`: Pre-aggregated metrics
- `carrier_performance`: Carrier reliability stats
- `user_activities`: User action logging
- `batch_operations`: Bulk operation tracking

**MCP Components Organization**:
```
backend/src/mcp/
├── __init__.py              # Main MCP server registration
├── tools/                   # MCP tools (callable functions)
│   ├── shipment_tools.py    # Create/list/get shipments
│   ├── tracking_tools.py    # Track packages
│   ├── rate_tools.py        # Get shipping rates
│   ├── bulk_tools.py        # Batch tracking
│   ├── bulk_creation_tools.py  # Parallel bulk shipment creation (16 workers)
│   └── flexible_parser.py   # Parse spreadsheet data
├── resources/               # MCP resources (data providers)
│   ├── shipment_resources.py  # List shipments
│   └── stats_resources.py     # Analytics statistics
└── prompts/                 # MCP prompts (AI templates)
    ├── shipping_prompts.py  # Shipment creation assistance
    ├── tracking_prompts.py  # Tracking queries
    ├── optimization_prompts.py  # Cost/route optimization
    └── comparison_prompts.py    # Carrier comparisons
```

### Frontend Structure

**Pages** (`frontend/src/pages/`):
- DashboardPage: Overview with quick actions
- ShipmentsPage: Create/manage shipments
- TrackingPage: Track packages
- AnalyticsDashboard: Metrics and insights
- SettingsPage: Configuration

**State Management**:
- TanStack Query for server state (caching, refetching)
- Zustand for local state (user preferences, UI state)
- React Hook Form + Zod for form validation

**API Integration** (`frontend/src/services/api.js`):
- Axios-based client with interceptors
- Base URL: `http://localhost:8000`
- Endpoints mirror backend routes

### Parallel Processing Architecture

The project uses hardware-optimized parallel processing in several areas:

**M3 Max Configuration** (16 performance cores):
- pytest: 16 parallel workers (pytest.ini: `-n 16`)
- Bulk creation: 16 parallel workers (bulk_creation_tools.py)
- Analytics: 16 chunks via asyncio.gather (server.py:344-376)
- ThreadPoolExecutor: 32-40 workers for I/O (easypost_service.py)
- Uvicorn production: 33 workers (2*16+1)
- PostgreSQL: 16 max_parallel_workers, 50 connection pool

**Key Files for Performance**:
- `backend/src/mcp/tools/bulk_creation_tools.py`: Parallel shipment creation
- `backend/src/server.py` (lines 305-377): Parallel analytics aggregation
- `backend/src/services/database_service.py`: Optimized database queries with eager loading
- `backend/tests/integration/test_bulk_performance.py`: Benchmarks
- `backend/pytest.ini`: Test parallelization config
- `database/postgresql-m3max.conf`: PostgreSQL M3 Max configuration

## Key Patterns

### Error Handling
- All async functions use try/except with detailed logging
- Request IDs added for tracing (`request.state.request_id`)
- Pydantic models for input validation
- FastAPI HTTPException for error responses

### Testing
- Backend: pytest with async support, fixtures in `conftest.py`
- Use `@pytest.mark.integration` for tests requiring live EasyPost API
- Mock EasyPost client in unit tests
- Frontend: Vitest with Testing Library
- Performance benchmarks compare sequential vs parallel execution

### Environment Variables
- `.env.development` (committed): Test API key (EZTK*)
- `.env.production` (gitignored): Live API key (EZAK*)
- `.env.example` (committed): Template
- Load via `ENVIRONMENT` variable or default to development
- `DATABASE_URL`: PostgreSQL connection string (postgresql+asyncpg://...)

### Database Patterns
- SQLAlchemy 2.0 async ORM with asyncpg driver
- Connection pooling: 20 base + 30 overflow = 50 total connections
- M3 Max optimizations: 32GB shared_buffers, 16 parallel workers
- Advanced indexing: composite, covering, and partial indexes
- Query optimization: selectinload() to prevent N+1 queries
- UUID v7 primary keys for better B-tree locality
- Async session management via FastAPI dependency injection
- Alembic for schema migrations

### Code Style
- Python: 100 char line length, snake_case, type hints required
- Black + Ruff for formatting/linting (config in pyproject.toml)
- JavaScript: ESLint + Prettier, camelCase
- See `.cursorrules` for universal command system and conventions

## MCP Integration

The project implements the Model Context Protocol for AI integration:

**Running MCP Server**:
```bash
cd backend && source venv/bin/activate
python -m src.mcp
```

**Available MCP Tools**:
- `create_shipment`: Create single shipment with label purchase
- `track_shipment`: Track by tracking number
- `get_rates`: Compare shipping rates
- `create_bulk_shipments`: Parallel bulk creation (16 workers, dry-run support)
- `batch_track_shipments`: Track multiple packages concurrently

**MCP Resources**:
- `shipment://list`: Recent shipments
- `stats://summary`: Analytics overview

**MCP Prompts**:
- Shipping optimization suggestions
- Carrier comparison analysis
- Package tracking assistance

## Custom Slash Commands

The project uses a universal command system defined in `.cursorrules` and `.cursor/commands/`:

**Project-Specific Shipping Commands**:
- `/bulk-create`: Bulk shipment creation with parallel processing
- `/carrier-compare`: AI carrier recommendations
- `/analytics-deep`: Parallel analytics with AI insights
- `/track-batch`: Batch tracking (50 packages in 2-3s)
- `/shipping-optimize`: AI strategy analysis

**Development Commands**:
- `/ep-test`: Run tests (16 parallel workers)
- `/ep-dev`: Start all servers concurrently
- `/ep-benchmark`: Performance benchmarks
- `/ep-lint`: Parallel linting
- `/ep-mcp`: MCP tool testing

**Universal Commands** (work across projects):
- `/fix`: Smart error fixing
- `/optimize`: Hardware-specific optimizations
- `/test [file]`: Generate comprehensive tests
- `/api [path] [method]`: Generate API endpoint

Commands are configured via `.dev-config.json` for project-specific behavior.

## Performance Characteristics

**Expected Throughput** (M3 Max):
- Bulk shipment creation: 3-4 shipments/second (100 in 30-40s)
- Batch tracking: 50 packages in 2-3s (16x speedup)
- Analytics processing: 1000 shipments in 1-2s (10x speedup)
- Test execution: 16 parallel workers

**Optimization Techniques**:
- uvloop for async I/O (2-4x faster than asyncio)
- ThreadPoolExecutor scaled to CPU cores
- asyncio.gather for concurrent operations
- Chunk-based parallel processing
- pytest-xdist for parallel testing

## Common Workflows

### Adding a Database Model
1. Add model to `backend/src/models.py` (SQLAlchemy model)
2. Create migration: `alembic revision -m "add new model"`
3. Edit migration file in `backend/alembic/versions/`
4. Run migration: `alembic upgrade head`
5. Add CRUD methods to `backend/src/services/database_service.py`
6. Add tests in `backend/tests/unit/test_database_service.py`
7. Add API endpoints if needed

### Adding a New MCP Tool
1. Create tool function in `backend/src/mcp/tools/new_tool.py`
2. Register in `backend/src/mcp/tools/__init__.py`
3. Add tests in `backend/tests/unit/test_new_tool.py`
4. Document in relevant prompts if AI-assisted

### Adding a Frontend Feature
1. Create component in `frontend/src/components/`
2. Add API call to `frontend/src/services/api.js`
3. Create page or integrate into existing page
4. Add route in main App component if needed
5. Write tests with Vitest + Testing Library

### Running Performance Benchmarks
```bash
cd backend && source venv/bin/activate
pytest tests/integration/test_bulk_performance.py -v
# Or via script:
./scripts/benchmark.sh
```

## Important Files

**Configuration**:
- `backend/pytest.ini`: Test configuration with parallel execution
- `backend/pyproject.toml`: Python tool configuration (black, ruff, mypy)
- `backend/alembic.ini`: Alembic migration configuration
- `database/postgresql-m3max.conf`: PostgreSQL M3 Max optimizations
- `frontend/package.json`: Frontend scripts and dependencies
- `.cursorrules`: Universal command system rules
- `Makefile`: Quick development commands

**Entry Points**:
- `backend/src/server.py`: FastAPI HTTP server
- `backend/src/mcp/__init__.py`: MCP server
- `frontend/src/main.jsx`: React app entry

**Core Logic**:
- `backend/src/services/easypost_service.py`: EasyPost API wrapper (32-40 workers)
- `backend/src/services/database_service.py`: PostgreSQL CRUD operations (548 lines)
- `backend/src/mcp/tools/bulk_creation_tools.py`: Parallel bulk operations
- `frontend/src/services/api.js`: API client

**Database**:
- `backend/src/database.py`: SQLAlchemy async engine and session config
- `backend/src/models.py`: Database models (9 tables)
- `backend/src/dependencies.py`: FastAPI database session dependency
- `backend/alembic/versions/`: Migration files
- `backend/alembic/env.py`: Alembic environment configuration

## Environment Setup Notes

- Python 3.10+ required (uses modern type hints)
- PostgreSQL 14+ required (uses modern features like covering indexes)
- Node.js for frontend (Vite requires Node 14+)
- EasyPost API key required (test or production)
- M3 Max optimizations assume 16+ cores (will work with fewer but slower)
- pytest-xdist requires `pytest -n auto` or `-n <workers>` for parallel execution
- Database URL format: `postgresql+asyncpg://user:password@localhost:5432/easypost_mcp`
- M3 Max PostgreSQL config in `database/postgresql-m3max.conf` (32GB buffers, 16 workers)

## Additional Documentation

For comprehensive PostgreSQL implementation details, see:
- `docs/architecture/POSTGRESQL_ARCHITECTURE.md`: Complete database architecture review
  - 9-table schema with advanced indexing
  - M3 Max-optimized configuration (32GB buffers, 16 parallel workers)
  - 548-line DatabaseService with CRUD operations
  - Connection pooling (50 total connections)
  - Query optimization techniques
  - Migration history and performance benchmarks

For historical implementation reports and status updates, see:
- `docs/archive/2025-11-implementation/`: Implementation phases, reports, and summaries
