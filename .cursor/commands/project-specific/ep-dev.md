Start EasyPost development environment (backend + frontend + MCP).

**Domain**: EasyPost MCP development
**Performance**: Concurrent startup on M3 Max

## Usage

```bash
# Start full stack
/ep-dev

# Backend only
/ep-dev backend

# Frontend only
/ep-dev frontend

# MCP server only
/ep-dev mcp

# With live reload
/ep-dev --watch

# Reset environment
/ep-dev --reset
```

## What It Does

**Concurrent Startup:**
1. Activates Python venv (backend)
2. Starts FastAPI with uvicorn (port 8000)
3. Starts React dev server (port 5173)
4. Starts MCP server (stdio)
5. Shows real-time logs from all services

## MCP Integration

**Server**: Desktop Commander
**Tool**: `start_process` (3 concurrent processes)

**Process 1 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn src.server:app --reload --host 0.0.0.0 --port 8000
```

**Process 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Process 3 - MCP Server:**
```bash
cd backend
source venv/bin/activate
python -m src.mcp
```

## Output Format

```
╔═══════════════════════════════════════════════════════════╗
║         EASYPOST DEVELOPMENT ENVIRONMENT                  ║
╚═══════════════════════════════════════════════════════════╝

🚀 Starting services...

[Backend] Starting FastAPI server...
[Frontend] Starting React dev server...
[MCP] Starting MCP server...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Services Running:

[Backend]
   URL: http://localhost:8000
   Docs: http://localhost:8000/docs
   Health: http://localhost:8000/health
   PID: 12345

[Frontend]
   URL: http://localhost:5173
   PID: 12346

[MCP]
   Protocol: stdio
   Tools: 15 registered
   Resources: 3 available
   PID: 12347

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 Live Logs (Ctrl+C to stop all services):

[Backend] INFO:     Uvicorn running on http://0.0.0.0:8000
[Frontend] VITE v5.0.0  ready in 432 ms
[Frontend] ➜  Local:   http://localhost:5173/
[MCP] INFO:     MCP server started with 15 tools
[Backend] INFO:     ThreadPoolExecutor: auto-detected workers
[Frontend] ➜  Network: http://192.168.1.100:5173/
```

## Smart Features

**Health Checks:**
- Waits for each service to be ready
- Verifies endpoints respond
- Shows clear error if startup fails

**Environment Validation:**
- Checks .env file exists
- Validates EASYPOST_API_KEY set
- Verifies dependencies installed

**Graceful Shutdown:**
- Ctrl+C stops all services
- Cleans up processes
- Saves logs to `.cursor/dev-logs/`

## Configuration

### Backend Settings
```python
# backend/src/utils/config.py
EASYPOST_API_KEY: from .env
WORKERS: auto-detected (max 16)
LOG_LEVEL: "info"
```

### Frontend Settings
```javascript
// frontend/vite.config.js
server: {
  port: 5173,
  host: true,
  hmr: { overlay: true }
}
```

### MCP Settings
```json
// claude_desktop_config.json
{
  "mcpServers": {
    "easypost-shipping": {
      "command": "python",
      "args": ["-m", "src.mcp"],
      "cwd": "backend"
    }
  }
}
```

## Troubleshooting

**Port already in use:**
```bash
/ep-dev --reset  # Kills existing processes and restarts
```

**Dependencies missing:**
```bash
cd backend && pip install -r requirements.txt
cd frontend && npm install
```

**Environment variables:**
```bash
# Check .env file
cat backend/.env

# Set if missing
echo "EASYPOST_API_KEY=your_key_here" >> backend/.env
```

## Advanced Usage

**Watch specific directories:**
```bash
# Only reload on backend changes
/ep-dev backend --watch-dir=src/

# Only reload on frontend changes
/ep-dev frontend --watch-dir=src/components/
```

**Debug mode:**
```bash
/ep-dev --debug
# Shows detailed logs, SQL queries, API calls
```

**Performance mode:**
```bash
/ep-dev --prod
# Uses production builds, no hot reload
```

## Related Commands

```bash
/ep-dev                # Start environment (this)
/ep-test               # Run tests
/ep-lint               # Check code quality
/ep-benchmark          # Run performance tests
```

**One command to rule them all - full dev environment in seconds!**
