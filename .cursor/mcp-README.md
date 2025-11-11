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

1. Set required environment variables in your shell (before starting Cursor IDE):
   ```bash
   export EASYPOST_API_KEY="your_key_here"
   export DATABASE_URL="postgresql+asyncpg://easypost:easypost@localhost:5432/easypost_mcp"
   ```
   
   **Note**: These environment variables are read from your shell environment. The MCP server will inherit them automatically.

2. Alternatively, load from `.env` file (recommended):
   ```bash
   # In project root
   source .env  # or use direnv if configured
   ```

3. The MCP server will automatically start when you open this project in Cursor IDE.

4. Access tools via the MCP menu or by using natural language commands.

## File Structure

```
.cursor/
├── mcp.json           # MCP server configuration (THIS FILE's config)
└── mcp-README.md      # This documentation
```

## Security

**Important**: The `.cursor/mcp.json` file does not contain hardcoded API keys or credentials. All sensitive values are read from your shell environment variables. This ensures:

- No secrets committed to version control
- Portability across different machines
- Easy rotation of API keys

**Required Environment Variables:**
- `EASYPOST_API_KEY` - Must be set in your shell environment
- `DATABASE_URL` - PostgreSQL connection string (optional for development)

Set these before starting Cursor IDE, or use a tool like `direnv` to load them automatically from `.env`.

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
2. Verify environment variables are set: `echo $EASYPOST_API_KEY`
3. Ensure variables are exported in your shell (not just in `.env` file)
4. Restart Cursor IDE after setting environment variables

**Python path issues:**
- The configuration uses workspace-relative paths (`${workspaceFolder}`) for portability
- Paths automatically resolve to your project location
- No need to update paths when moving the project directory
- **Note**: If `${workspaceFolder}` is not supported in your Cursor version, replace with absolute paths:
  ```json
  "command": "/absolute/path/to/project/backend/venv/bin/python"
  ```

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
