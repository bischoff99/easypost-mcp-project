# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

EasyPost MCP is a **personal-use** backend-only shipping integration with:

- **Backend**: FastAPI + FastMCP server for EasyPost API integration
- **MCP Tools**: AI agent tools for shipment creation, tracking, and rate comparison
- **Data**: Direct EasyPost API integration (no database)

> **Note**: Enterprise features (webhooks, database persistence, frontend, bulk API operations) have been removed for personal use. The core MCP server functionality remains intact.

## Development Commands

### Quick Start

```bash
# Start backend server
make dev

# Or manually:
source venv/bin/activate && uvicorn src.server:app --reload
```

### Testing

```bash
# All tests (auto-detected parallel workers)
make test

# Coverage report
make test COV=1

# Run single backend test
pytest tests/path/to/test_file.py::test_function_name -v
```

### Code Quality

```bash
# Lint
make lint

# Auto-format (ruff for Python)
make format

# Full check (lint + test)
make check
```

### Database

**Note:** Database has been removed for personal use (YAGNI principle). All data is ephemeral and fetched directly from EasyPost API when needed.

### Production

```bash
# Build production bundles
make build

# Run production locally
make prod
```

## Architecture

### Backend Structure

```
src/
├── server.py           # FastAPI app with MCP integration
├── routers/            # API endpoints (shipments, tracking, analytics - simplified)
├── services/           # Business logic (easypost_service only - database removed)
├── models/             # Pydantic request/response models
├── mcp_server/         # FastMCP tools, prompts, and resources (core product)
│   ├── tools/          # MCP tools for AI agents
│   ├── prompts/        # Prompt templates
│   └── resources/      # Resource providers
├── lifespan.py         # App startup/shutdown lifecycle
└── utils/              # Config, monitoring, helpers
```

### Data Strategy (Personal Use - No Database)

**Direct EasyPost API Integration:**

- All shipment data fetched directly from EasyPost API
- No local persistence or caching (YAGNI principle)
- Simpler architecture with fewer dependencies
- Example: `service = EasyPostService(api_key); shipment = await service.create_shipment(data)`

> **Note**: Database (PostgreSQL, SQLAlchemy, Alembic) has been completely removed for personal use. All data is ephemeral and retrieved from EasyPost API on-demand.

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

- **Removed for personal use (YAGNI)** - All data retrieved directly from EasyPost API
- No local persistence, migrations, or connection pooling needed
- Simplified architecture with fewer dependencies

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

## Important Configuration Files

- **Backend**:
  - `config/pyproject.toml`: Ruff, Black, mypy configuration
  - `pytest.ini`: Test configuration with auto-detected parallel workers
  - `config/requirements.txt`: Production dependencies with version ranges
  - `config/.env*`: Environment variables (EASYPOST_API_KEY)

- **Root**:
  - `Makefile`: Quick development commands
  - `.cursor/rules/`: Comprehensive coding standards (see 00-INDEX.mdc)

## Optimizations

This project uses simple, effective optimizations:

- **Backend**: Auto-detected pytest workers, async I/O, direct API integration
- **Testing**: Parallel execution with auto-detected workers
- **Architecture**: Database removed (YAGNI) - simpler, fewer dependencies

## Common Workflows

### Adding a New API Endpoint

1. Create route in `src/routers/`
2. Define Pydantic request/response models in `src/models/requests.py`
3. Implement business logic in service layer (`services/`)
4. Add tests in `tests/`

### Adding a New MCP Tool

1. Create tool function in `src/mcp_server/tools/`
2. Decorate with `@mcp.tool()` and add comprehensive docstring
3. Register in `src/mcp_server/tools/__init__.py`
4. Add tests with 100% coverage requirement
5. Document in `docs/guides/MCP_TOOLS_USAGE.md`

## Coding Standards

**Critical rules** (see `.cursor/rules/` for comprehensive details):

1. **Type Safety**: Type hints required for all Python functions
2. **Error Handling**: Raise errors explicitly, never silently ignore failures
3. **Async Operations**: Use async/await for all I/O operations
4. **Testing**: AAA pattern, mock external APIs, parametrized tests
5. **Security**: No hardcoded secrets, parameterized queries, input validation

**Import Sorting** (handled by Ruff):

- Future imports
- Standard library
- Third-party (fastapi, pydantic, easypost)
- First-party (src.\*)
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
    "easypost-test": {
      "command": "/path/to/repo/venv/bin/python",
      "args": ["/path/to/repo/scripts/python/run_mcp.py"],
      "cwd": "/path/to/repo",
      "env": { "ENVIRONMENT": "test" }
    },
    "easypost-prod": {
      "command": "/path/to/repo/venv/bin/python",
      "args": ["/path/to/repo/scripts/python/run_mcp.py"],
      "cwd": "/path/to/repo",
      "env": { "ENVIRONMENT": "production" }
    }
  }
}
```

## Documentation

- **Project Guides**: `docs/guides/`
  - `BENCHMARKING.md`: Performance testing
  - `MCP_BASH_INTEGRATION.md`: Shell integration
  - `MCP_ENVIRONMENT_SWITCHING.md`: Environment management
  - `WORKFLOW_USAGE_GUIDE.md`: Development workflows

- **Architecture**: `docs/architecture/`
  - `FASTMCP_STRUCTURE.md`: MCP server architecture
  - `MCP_TOOLS_INVENTORY.md`: Available MCP tools
  - `decisions/`: Architectural decision records

- **Cursor Rules**: `.cursor/rules/`
  - `00-INDEX.mdc`: Complete rules index
  - `01-fastapi-python.mdc`: Backend best practices
  - `02-testing-best-practices.mdc`: Testing strategy
  - `03-mcp-development.mdc`: MCP tool development
  - `04-m3-max-optimizations.mdc`: Performance optimization

## Environment Setup

**Backend**:

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r config/requirements.txt

# 3. Store API keys in macOS Keychain (RECOMMENDED)
security add-generic-password -s "easypost-test" -a "${USER}" -w "YOUR_TEST_KEY"
security add-generic-password -s "easypost-prod" -a "${USER}" -w "YOUR_PROD_KEY"

# 4. Setup direnv (optional but recommended)
brew install direnv
echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc
direnv allow

# API keys are automatically loaded from Keychain via .envrc
# See config/.env.example for alternative setup methods
```

**Note**: API keys are stored securely in macOS Keychain and loaded automatically by direnv. The [.envrc](.envrc) file handles environment-specific key loading based on `ENVIRONMENT` variable (test/production).

## URLs

- Backend API: http://localhost:8000
- Health Check: http://localhost:8000/health
- API Docs: http://localhost:8000/docs

## Troubleshooting

**Backend issues:**

- Check logs: Backend logs to stdout with structured logging
- EasyPost API: Ensure `EASYPOST_API_KEY` is valid (test/production)

**Test failures:**

- Run serially for debugging: `pytest tests/file.py -v` (without `-n auto`)
- Check mocks: Ensure EasyPost API calls are mocked
- View coverage: `make test COV=1` then open `htmlcov/index.html`
