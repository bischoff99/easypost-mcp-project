# EasyPost MCP - Documentation Index

**Complete documentation for the EasyPost shipping integration project.**

---

## Quick Start

**New to the project?** Start here:
1. [Setup Instructions](setup/START_HERE.md) - Get up and running
2. [Environment Setup](setup/ENVIRONMENT_SETUP.md) - Configure your dev environment
3. [Workflows Guide](WORKFLOWS_GUIDE.md) - Daily development workflows

---

## Documentation Structure

### Architecture
High-level system design and patterns.

- [PostgreSQL Architecture](architecture/POSTGRESQL_ARCHITECTURE.md) - Database design and optimization
- [MCP Tools Inventory](architecture/MCP_TOOLS_INVENTORY.md) - Available MCP tools
- [Structure Optimization](architecture/STRUCTURE_OPTIMIZATION.md) - Project organization

### Guides
How-to guides for specific tasks.

- [Deployment Guide](guides/DEPLOYMENT.md) - Production deployment
- [Development Deployment](guides/DEV_DEPLOYMENT_GUIDE.md) - Local development setup
- [Monitoring Guide](guides/MONITORING.md) - Health checks and metrics
- [M3 Max Optimizations](guides/M3_MAX_OPTIMIZATION_REPORT.md) - Performance tuning
- [Optional Optimizations](guides/OPTIONAL_OPTIMIZATIONS.md) - Enhancement suggestions
- [PostgreSQL Best Practices](guides/POSTGRESQL_BEST_PRACTICES.md) - Database patterns
- [Proxy Integration](guides/PROXY_AND_DATABASE_INTEGRATION.md) - Nginx setup
- [Proxy Benefits](guides/PROXY_BENEFITS.md) - Why use a reverse proxy
- [Quick Reference](guides/QUICK_REFERENCE.md) - Command cheat sheet
- [Shell Integration](../SHELL_INTEGRATION.md) - Terminal productivity
- [Slash Commands Setup](guides/SLASH_COMMANDS_SETUP.md) - Cursor IDE commands
- [Universal Commands](guides/UNIVERSAL_COMMANDS.md) - Cross-project commands
- [Bulk Tool Usage](guides/BULK_TOOL_USAGE.md) - Parallel processing
- [Database Integration](guides/DATABASE_INTEGRATION_IMPLEMENTATION.md) - DB setup

### Setup
Getting started with the project.

- [Start Here](setup/START_HERE.md) - Quick start guide
- [Environment Setup](setup/ENVIRONMENT_SETUP.md) - Environment variables
- [Setup Instructions](setup/SETUP_INSTRUCTIONS.md) - Detailed setup

### Workflows
Development workflows and automation.

- [Workflows Guide](WORKFLOWS_GUIDE.md) - Make command workflows
- [Shell Integration](../SHELL_INTEGRATION.md) - Terminal shortcuts

### Archive
Historical documents and reports.

- [2025-11-03](archive/2025-11-03/) - Initial implementation
- [2025-11-03-cleanup](archive/2025-11-03-cleanup/) - First cleanup
- [2025-11-implementation](archive/2025-11-implementation/) - Full implementation
- [2025-11-04](archive/2025-11-04/) - Latest cleanup and reorganization

---

## Key Documents

### Must Read
1. **[README.md](../README.md)** - Project overview
2. **[CLAUDE.md](../CLAUDE.md)** - AI assistant development guide
3. **[Workflows Guide](WORKFLOWS_GUIDE.md)** - 25 Make commands
4. **[Shell Integration](../SHELL_INTEGRATION.md)** - Terminal productivity

### Architecture
- **[PostgreSQL Architecture](architecture/POSTGRESQL_ARCHITECTURE.md)** - Database design
- **[MCP Tools Inventory](architecture/MCP_TOOLS_INVENTORY.md)** - Available tools

### Operations
- **[Deployment](guides/DEPLOYMENT.md)** - Production deployment
- **[Monitoring](guides/MONITORING.md)** - Health checks and metrics
- **[M3 Max Optimizations](guides/M3_MAX_OPTIMIZATION_REPORT.md)** - Performance

---

## Quick Links

### Development
```bash
make dev           # Start servers
make test          # Run tests
make check         # Quality checks
```

### Documentation
```bash
# View in browser
open docs/README.md
open docs/guides/QUICK_REFERENCE.md
open ../README.md
```

### Get Help
```bash
make help          # See all make commands
ep-help            # Shell integration commands (if installed)
```

---

## Documentation by Role

### For New Developers
1. [Start Here](setup/START_HERE.md)
2. [Environment Setup](setup/ENVIRONMENT_SETUP.md)
3. [Workflows Guide](WORKFLOWS_GUIDE.md)
4. [Shell Integration](../SHELL_INTEGRATION.md)

### For DevOps/SRE
1. [Deployment Guide](guides/DEPLOYMENT.md)
2. [PostgreSQL Architecture](architecture/POSTGRESQL_ARCHITECTURE.md)
3. [Monitoring Guide](guides/MONITORING.md)
4. [Proxy Integration](guides/PROXY_AND_DATABASE_INTEGRATION.md)

### For Performance Engineers
1. [M3 Max Optimizations](guides/M3_MAX_OPTIMIZATION_REPORT.md)
2. [Optional Optimizations](guides/OPTIONAL_OPTIMIZATIONS.md)
3. [PostgreSQL Best Practices](guides/POSTGRESQL_BEST_PRACTICES.md)

### For AI/MCP Developers
1. [MCP Tools Inventory](architecture/MCP_TOOLS_INVENTORY.md)
2. [Bulk Tool Usage](guides/BULK_TOOL_USAGE.md)
3. [Database Integration](guides/DATABASE_INTEGRATION_IMPLEMENTATION.md)

---

## Contributing

See [CLAUDE.md](../CLAUDE.md) for:
- Coding standards
- Testing requirements
- Commit conventions
- Development workflow

---

**Last Updated:** November 5, 2025
