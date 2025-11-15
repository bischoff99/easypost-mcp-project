# /ep-dev (Deprecated)

The repository now runs a single FastAPI + MCP backend. The old `/ep-dev` command
that tried to launch backend + React frontend is no longer maintained.

## Replacement commands

```bash
# Create venv + install deps
make setup

# Start backend (with auto reload)
make dev
# or
source venv/bin/activate && uvicorn src.server:app --reload --host 0.0.0.0 --port 8000

# Run MCP server only
source venv/bin/activate && python scripts/python/run_mcp.py

# Quick regression check
./scripts/test/quick-test.sh

# Full lint + test battery
make check
```

Use these instead of `/ep-dev`. If you still need a custom launcher, update this
command to wrap the current backend-only workflow.
