# EasyPost MCP - Documentation Index

**Complete documentation for the EasyPost shipping integration project.**

---

## Quick Start

**New to the project?** Start here:
1. [README.md](../README.md) - Project overview and setup
2. [CLAUDE.md](../CLAUDE.md) - Development guide for AI assistants

---

## Documentation Structure

### Architecture
High-level system design and patterns.

- [FastMCP Structure](architecture/FASTMCP_STRUCTURE.md) - MCP server architecture
- [MCP Tools Inventory](architecture/MCP_TOOLS_INVENTORY.md) - Available MCP tools
- [Build Commands Optimization](architecture/BUILD_COMMANDS_OPTIMIZATION.md) - Development workflow optimization
- [Optimization Summary](architecture/OPTIMIZATION_SUMMARY.md) - Performance improvements

### Architecture Decisions
Key architectural decisions documented as ADRs.

- [ADR-001: Router Organization](architecture/decisions/ADR-001-router-organization.md) - API routing structure
- [ADR-002: M3 Max Optimization](architecture/decisions/ADR-002-m3-max-optimization.md) - Performance tuning

### Guides
How-to guides for specific tasks.

- [Benchmarking](guides/BENCHMARKING.md) - Performance testing
- [MCP Bash Integration](guides/MCP_BASH_INTEGRATION.md) - Shell integration for MCP tools
- [MCP Environment Switching](guides/MCP_ENVIRONMENT_SWITCHING.md) - Test/production environments
- [Workflow Bash Integration](guides/WORKFLOW_BASH_INTEGRATION.md) - Terminal workflows
- [Workflow Usage Guide](guides/WORKFLOW_USAGE_GUIDE.md) - Development workflows

### API Testing
- [API Requests](api-requests.http) - HTTP request examples for testing

---

## Key Documents

### Must Read
1. **[README.md](../README.md)** - Project overview and quick start
2. **[CLAUDE.md](../CLAUDE.md)** - AI assistant development guide
3. **[Makefile](../Makefile)** - Development commands (`make help`)

### Architecture
- **[FastMCP Structure](architecture/FASTMCP_STRUCTURE.md)** - MCP server architecture
- **[MCP Tools Inventory](architecture/MCP_TOOLS_INVENTORY.md)** - Available MCP tools

### Development
- **[MCP Environment Switching](guides/MCP_ENVIRONMENT_SWITCHING.md)** - Environment management
- **[Workflow Usage Guide](guides/WORKFLOW_USAGE_GUIDE.md)** - Development workflows
- **[Benchmarking](guides/BENCHMARKING.md)** - Performance testing

---

## Quick Links

### Development
```bash
make dev           # Start backend server
make test          # Run tests
make check         # Quality checks (lint + test)
make help          # See all commands
```

### API Testing
```bash
# Use api-requests.http file with REST Client extension
# Or use curl/httpie directly
curl http://localhost:8000/health
```

---

## Documentation by Role

### For New Developers
1. [README.md](../README.md) - Project overview
2. [CLAUDE.md](../CLAUDE.md) - Development guide
3. [MCP Tools Inventory](architecture/MCP_TOOLS_INVENTORY.md) - Available tools

### For MCP Developers
1. [FastMCP Structure](architecture/FASTMCP_STRUCTURE.md) - Architecture
2. [MCP Tools Inventory](architecture/MCP_TOOLS_INVENTORY.md) - Tool reference
3. [MCP Environment Switching](guides/MCP_ENVIRONMENT_SWITCHING.md) - Environments

### For Performance Engineers
1. [Optimization Summary](architecture/OPTIMIZATION_SUMMARY.md) - Performance improvements
2. [Build Commands Optimization](architecture/BUILD_COMMANDS_OPTIMIZATION.md) - Workflow optimization
3. [Benchmarking](guides/BENCHMARKING.md) - Testing methodology

---

## Contributing

See [CLAUDE.md](../CLAUDE.md) for:
- Coding standards
- Testing requirements
- Commit conventions
- Development workflow

---

**Note:** This is a personal-use, backend-only project. Database persistence and frontend have been removed. All data is fetched directly from EasyPost API on-demand.
