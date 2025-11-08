# Project MCP Configuration

This file documents the project-specific MCP (Model Context Protocol) server configuration for Cursor IDE.

## Purpose

The `.cursor/mcp.json` file defines MCP servers that are specific to this project. These servers are automatically loaded when you open this project in Cursor IDE.

## Configuration

### easypost-shipping

The main MCP server for this project, providing tools to interact with the EasyPost shipping API.

**Features:**
- Create and manage shipments
- Generate shipping labels
- Track packages
- Manage addresses
- Calculate shipping rates
- Batch operations support

**Environment Variables Required:**
- `EASYPOST_API_KEY` - Your EasyPost API key (test or production)
- `DATABASE_URL` - PostgreSQL database connection string

**Setup:**

1. Ensure you have the EasyPost API key in your environment:
   ```bash
   export EASYPOST_API_KEY="your_key_here"
   ```

2. The MCP server will automatically start when you open this project in Cursor IDE.

3. Access tools via the MCP menu or by using natural language commands.

## File Structure

```
.cursor/
├── mcp.json           # MCP server configuration (THIS FILE's config)
└── mcp-README.md      # This documentation
```

## Global vs Project MCP

**Global MCP** (`~/.cursor/mcp.json`):
- Shared across all projects
- Contains user-level MCP servers (Desktop Commander, GitHub, Context7, Neo4j, etc.)

**Project MCP** (`.cursor/mcp.json`):
- Project-specific servers
- Automatically loaded when opening this project
- Inherits and extends global configuration

## Troubleshooting

**Server not starting:**
1. Check that the virtual environment exists: `backend/venv/bin/python`
2. Verify the API key is set: `echo $EASYPOST_API_KEY`
3. Restart Cursor IDE

**Python path issues:**
- The configuration uses absolute paths to ensure reliability
- Update paths if you move the project directory

**Database connection:**
- Ensure PostgreSQL is running: `pg_isready`
- Check the database exists: `psql -l | grep easypost_mcp`

## Documentation

- Full MCP tool documentation: `docs/architecture/MCP_TOOLS_INVENTORY.md`
- MCP usage guide: `docs/guides/MCP_TOOLS_USAGE.md`
- Development setup: `docs/setup/START_HERE.md`

## Related Files

- `.cursor/commands/project-specific/ep-dev.md` - Development environment command
- `backend/run_mcp.py` - MCP server entry point
- `backend/src/mcp_server/` - MCP server implementation
