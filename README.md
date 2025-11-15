# EasyPost MCP Project

**Personal-use** EasyPost shipping integration with MCP server (backend-only).

> **Note**: This project has been simplified for personal use. Enterprise features (webhooks, database persistence, frontend) have been removed. The core MCP server functionality remains intact.

## Quick Start

### 1. Clone and Setup Environment

```bash
git clone <repository-url>
cd easypost-mcp-project
cp .env.example .env
# Edit .env with your EasyPost API key
```

### 2. Install Dependencies

```bash
make setup
# Or manually:
# python3 -m venv venv && source venv/bin/activate && pip install -r config/requirements.txt
```

### 3. Start Development Servers

```bash
make dev
# Starts backend server on http://localhost:8000
```

## URLs

- Backend API: http://localhost:8000
- Health Check: http://localhost:8000/health
- API Docs: http://localhost:8000/docs

## Project Structure

```
easypost-mcp-project/
├── src/                  # FastAPI + FastMCP source code
│   ├── mcp_server/       # MCP tools (core product)
│   ├── routers/          # API endpoints (optional, for testing)
│   └── services/         # Business logic (EasyPost only)
├── tests/                # Test suite (unit + integration)
├── config/               # pyproject, requirements, environment files
├── data/                 # Sample data exports (gitignored)
├── deploy/               # Docker Compose configurations
├── docs/                 # Project documentation
├── scripts/              # Utility scripts (dev/test/ops)
└── venv/                 # Local Python virtual environment (personal use)
└── scripts/              # Utility scripts
```

## Features

### Core Features (Personal Use)

✅ **MCP Server** - AI agent tools for shipment management (core product)
✅ **Basic API** - Simple FastAPI endpoints for testing
✅ **Error handling** - Comprehensive error handling
✅ **Input validation** - Pydantic validation
✅ **Logging** - Structured logging

### Removed (Enterprise Features)

❌ Frontend/Web UI
❌ Webhook system
❌ Database persistence (all data from EasyPost API)
❌ Bulk operations endpoints (use MCP tools instead)
❌ Request ID middleware (disabled by default)

## Architecture

### MCP Server (Core Product)

The MCP server provides AI agent tools for:

- Creating shipments
- Getting rates
- Tracking shipments
- Bulk operations (via MCP tools, not API endpoints)

**Location**: `src/mcp_server/`
**Endpoint**: `/mcp` (HTTP transport)

### FastAPI Backend (Optional Testing Interface)

Optional HTTP API endpoints for testing:

- `/api/rates` - Get shipping rates
- `/api/shipments` - Create and manage shipments
- `/api/tracking` - Track shipments

### Data Architecture

- **No database** - Removed for personal use (YAGNI principle)
- **Direct EasyPost API** - All data fetched on-demand
- **Simpler architecture** - Fewer dependencies, easier maintenance

## Documentation

- **[CLAUDE.md](CLAUDE.md)** - Comprehensive guide for AI assistants
- **[Commands README](.cursor/commands/README.md)** - Universal slash commands system
- **[Current Workflows](.cursor/commands/WORKFLOWS-CURRENT.md)** - Working make commands
- **[Quick Reference](docs/guides/QUICK_REFERENCE.md)** - Code templates and patterns

## Development

### Testing

```bash
make test             # Run all tests
make test-fast        # Fast tests (changed files only)
make test-cov         # Coverage report
```

### Code Quality

```bash
make lint             # Lint code
make format           # Auto-format
make check            # Lint + test
```

## MCP Server Usage

The MCP server can be used with Claude Desktop or other MCP clients:

```json
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

## Simplifications for Personal Use

This project has been optimized for personal use by removing:

1. **Frontend/Web UI** - Backend-only MCP server for AI agents
2. **Webhook system** - Not needed for personal use
3. **Database persistence** - All data fetched directly from EasyPost API
4. **Bulk operations API** - Use MCP tools instead
5. **Request ID middleware** - Disabled by default (set `DEBUG=true` to enable)

**Result**: Lean backend-only codebase focused on MCP server functionality.
