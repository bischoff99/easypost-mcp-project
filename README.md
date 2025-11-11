# EasyPost MCP Project

Production-ready EasyPost shipping integration with MCP server and React frontend.

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
# cd backend && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
# cd frontend && npm install
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

## Features
✅ CORS configured
✅ Error handling
✅ Async/await
✅ Input validation
✅ Logging

## Architecture & Integration

### PostgreSQL Database (Dual-Pool Strategy)
- **SQLAlchemy ORM Pool:** 50 connections (CRUD operations)
- **asyncpg Direct Pool:** 32 connections (bulk operations)
- **M3 Max Optimized:** 82 total connections
- **Production-ready:** Handles 1000+ req/s

### Reverse Proxy (Optional - Production)
- **nginx configuration:** Single URL, no CORS
- **Performance:** 20x faster static asset delivery
- **Setup:** `bash scripts/setup-nginx-proxy.sh`
- **Benefits:** Edge rate limiting, browser caching

### Documentation
- **[CLAUDE.md](CLAUDE.md)** - Comprehensive guide for AI assistants (Claude Code, Cursor, etc.)
- **[Complete Integration Guide](docs/guides/PROXY_AND_DATABASE_INTEGRATION.md)** - Architecture, usage patterns, deployment
- **[Quick Reference](docs/guides/QUICK_REFERENCE.md)** - Code templates, commands, troubleshooting
- **[Architecture Diagrams](ARCHITECTURE_DIAGRAM.md)** - Visual data flow and request patterns
- **[Proxy Benefits](docs/guides/PROXY_BENEFITS.md)** - Detailed proxy analysis

### Workflows & Commands
- **[✅ Current Workflows](.cursor/commands/WORKFLOWS-CURRENT.md)** - All working make commands & development patterns
- **[🔴 Future Workflows](.cursor/commands/WORKFLOW-EXAMPLES.md)** - Aspirational workflow templates (24% implemented)
- **[Makefile](Makefile)** - 25+ quick development commands (`make help` to see all)
