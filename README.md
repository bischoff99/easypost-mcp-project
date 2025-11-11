# EasyPost MCP Project

**Personal-use** EasyPost shipping integration with MCP server and React frontend.

> **Note**: This project has been simplified for personal use. Enterprise features (webhooks, database-backed endpoints, bulk operations) have been removed. The core MCP server functionality remains intact.

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
make install
# Or manually:
# cd apps/backend && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
# cd apps/frontend && pnpm install
```

### 3. Start Development Servers
```bash
make dev
# Or separately:
# make backend   # Backend on http://localhost:8000
# make frontend   # Frontend on http://localhost:5173
```

## URLs
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- Health: http://localhost:8000/health
- API Docs: http://localhost:8000/docs

## Project Structure

```
easypost-mcp-project/
├── apps/
│   ├── backend/      # FastAPI/Python backend service
│   │   ├── src/      # Source code
│   │   │   ├── mcp_server/  # MCP tools (core product)
│   │   │   ├── routers/     # API endpoints (simplified)
│   │   │   └── services/     # Business logic
│   │   ├── tests/    # Test suite (unit + integration)
│   │   └── alembic/  # Database migrations
│   └── frontend/     # React/Vite frontend service
│       ├── src/      # Source code
│       └── tests/    # Tests
├── deploy/           # Docker Compose configurations
├── docs/             # Project documentation
└── scripts/          # Utility scripts
```

## Features

### Core Features (Personal Use)
✅ **MCP Server** - AI agent tools for shipment management (core product)  
✅ **Basic API** - Simple FastAPI endpoints for frontend  
✅ **React Frontend** - Management interface  
✅ **Simplified Analytics** - Basic shipping statistics  
✅ **Error handling** - Comprehensive error handling  
✅ **Input validation** - Pydantic validation  
✅ **Logging** - Structured logging  

### Removed (Enterprise Features)
❌ Webhook system  
❌ Database-backed endpoints (`/api/db/*`)  
❌ Bulk operations endpoints (use MCP tools instead)  
❌ Complex parallel analytics processing  
❌ Request ID middleware (disabled by default)  

## Architecture

### MCP Server (Core Product)
The MCP server provides AI agent tools for:
- Creating shipments
- Getting rates
- Tracking shipments
- Bulk operations (via MCP tools, not API endpoints)

**Location**: `apps/backend/src/mcp_server/`  
**Endpoint**: `/mcp` (HTTP transport)

### FastAPI Backend (Management Interface)
Simplified API for the React frontend:
- `/api/rates` - Get shipping rates
- `/api/shipments` - Create and manage shipments
- `/api/tracking` - Track shipments
- `/api/analytics` - Basic shipping statistics

### Database
- **SQLAlchemy ORM** - Single pool for CRUD operations
- **PostgreSQL** - Stores shipment data for MCP tool context
- Database models remain for MCP tools that need context

### Frontend
- **React 19** + **Vite 7.2** + **TailwindCSS 4**
- Pages: Dashboard, Shipments, Analytics, Tracking
- Simplified UI focused on core functionality

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

### Database
```bash
make db-reset         # Reset database
make db-upgrade       # Apply migrations
```

## MCP Server Usage

The MCP server can be used with Claude Desktop or other MCP clients:

```json
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

## Simplifications for Personal Use

This project has been optimized for personal use by removing:
1. **Webhook system** - Not needed for personal use
2. **Database-backed endpoints** - Use EasyPost API directly
3. **Bulk operations API** - Use MCP tools instead
4. **Complex analytics** - Simplified to sequential processing
5. **Request ID middleware** - Disabled by default (set `DEBUG=true` to enable)

**Result**: Leaner codebase focused on core MCP functionality while maintaining a simple management interface.
