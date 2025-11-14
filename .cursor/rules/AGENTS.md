# Agent Rules for EasyPost MCP Project

## Project Context

EasyPost MCP (Model Context Protocol) server integration. Multi-tier architecture with backend services, shipping API integration, and database management.

## Code Style & Standards

- Python: Follow PEP 8, use type hints, 4-space indentation, 100-char line limit
- Use Ruff formatter exclusively for Python (`editor.defaultFormatter: charliermarsh.ruff`)
- JavaScript/TypeScript: 2-space indentation, 100-char line limit, Prettier formatter
- All imports must be organized (isort for Python, ESLint for JS)

## Architecture Principles

- MCP server pattern: stdio transport for local, HTTP/SSE for distributed
- Database connections pooled via PostgreSQL service
- Vector embeddings managed through Chroma MCP
- Neo4j for knowledge graphs (cypher-based queries)
- Maintain isolation between backend/frontend layers

## Testing Requirements

- Python: pytest for unit tests, pytest coverage for integration tests
- Tests in `apps/backend/tests/` directory
- Minimum 50% coverage target (track in CI/CD)
- Mock external APIs (EasyPost, Neo4j, Chroma) in unit tests

## MCP Configuration

- All MCP servers defined in `.cursor/mcp.json`
- Credentials stored in environment variables (never in config)
- Path environment handling delegated to `~/.zprofile`
- Transport types: stdio for local dev, HTTP for production

## Before Making Changes

1. Understand current test coverage (check CI status)
2. Run `pytest apps/backend/tests/` locally before agent commits
3. Verify MCP server health (check logs in `.logs/`)
4. For database changes: create migrations, never direct schema edits

## File Pattern Attachments

- `@apps/backend/src/models.py` — Core data structures
- `@apps/backend/src/services/easypost_service.py` — API integration logic
- `.cursor/mcp.json` — MCP server definitions
- `.vscode/settings.json` — Project IDE configuration
