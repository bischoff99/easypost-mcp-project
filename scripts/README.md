# Scripts Directory

Helper scripts for development, testing, and maintenance of the EasyPost MCP project.

## Development Scripts

### `start-dev.sh`
Start both backend and frontend servers in separate terminal windows (macOS only).

```bash
./scripts/start-dev.sh
```

**What it does:**
- Opens new Terminal window for backend (port 8000)
- Opens new Terminal window for frontend (port 5173)
- Shows URLs and test commands

**URLs:**
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Frontend: http://localhost:5173

**Requirements:** macOS Terminal

---

### `start-backend.sh`
Start only the backend FastAPI server.

```bash
./scripts/start-backend.sh
```

**What it does:**
- Activates Python virtual environment
- Starts uvicorn with hot reload
- Port: 8000

---

### `start-backend-jit.sh`
Start backend with JIT compilation optimizations.

```bash
./scripts/start-backend-jit.sh
```

**What it does:**
- Similar to `start-backend.sh`
- Enables Python JIT optimizations
- Faster startup and runtime

---

### `start-frontend.sh`
Start only the frontend Vite development server.

```bash
./scripts/start-frontend.sh
```

**What it does:**
- Starts Vite dev server with hot reload
- Port: 5173

---

## Testing Scripts

### `quick-test.sh`
Run quick test suite for both backend and frontend.

```bash
./scripts/quick-test.sh
```

**What it does:**
- Backend: Runs pytest with minimal output
- Frontend: Runs Vitest in run mode
- Shows test results summary

**Duration:** ~30-60 seconds (depending on test count)

---

### `watch-tests.sh`
Run tests in watch mode for active development.

```bash
./scripts/watch-tests.sh
```

**What it does:**
- Backend: Starts pytest-watch (re-runs on file changes)
- Frontend: Starts Vitest in watch mode
- Useful for TDD workflow

**Stop:** Ctrl+C

---

### `benchmark.sh`
Run comprehensive performance benchmarks (M3 Max optimized).

```bash
./scripts/benchmark.sh
```

**What it does:**
- System information (CPU, RAM, cores)
- Backend performance:
  - ThreadPoolExecutor worker calculation
  - Build speed
  - Test speed (parallel)
- Frontend performance:
  - Build speed (Vite)
  - Test speed
- Docker build speed (if available)
- Performance summary with expected gains

**Output:** Detailed performance metrics
**Duration:** 2-5 minutes

---

## Additional Development Scripts

### `dev.sh` / `dev_local.sh`
Alternative development startup scripts.

```bash
./scripts/dev.sh
# or
./scripts/dev_local.sh
```

**What they do:**
- Start PostgreSQL Docker container
- Setup and start backend server
- Setup and start frontend server
- Handle cleanup on exit

**Difference:** `dev_local.sh` includes more error checking and user feedback

---

### `start-prod.sh`
Start production servers.

```bash
./scripts/start-prod.sh
```

**What it does:**
- Starts backend in production mode
- Starts frontend production build
- Uses production environment variables

---

## Utility Scripts

### `monitor-database.sh`
Monitor PostgreSQL database activity.

```bash
./scripts/monitor-database.sh
```

**What it does:**
- Shows active connections
- Displays query statistics
- Monitors database performance

---

### `setup-nginx-proxy.sh`
Setup Nginx reverse proxy for production.

```bash
./scripts/setup-nginx-proxy.sh
```

**What it does:**
- Configures Nginx for frontend/backend routing
- Sets up SSL certificates (if available)
- Configures proxy headers

---


### `test-full-functionality.sh`
Run comprehensive functionality tests.

```bash
./scripts/test-full-functionality.sh
```

**What it does:**
- Runs full test suite
- Tests API endpoints
- Validates database operations
- Checks frontend functionality

---

### `get-bulk-rates.py`
Python script for bulk rate testing.

```bash
python scripts/get-bulk-rates.py
```

**What it does:**
- Tests bulk shipment rate retrieval
- Validates bulk operations
- Useful for debugging bulk tools

---

### `verify_mcp_server.py`
Verify MCP server configuration.

```bash
python scripts/verify_mcp_server.py
```

**What it does:**
- Validates MCP server setup
- Tests tool registration
- Checks resource providers

---

## Usage Examples

### Quick Development Start
```bash
# Option 1: Use Makefile (from root)
make dev

# Option 2: Use script
./scripts/start-dev.sh
```

### Testing Workflow
```bash
# Quick test before commit
./scripts/quick-test.sh

# Watch mode during development
./scripts/watch-tests.sh

# Performance benchmarks
./scripts/benchmark.sh
```

### Utility Workflow
```bash
# Monitor database
./scripts/monitor-database.sh

# Test full functionality
./scripts/test-full-functionality.sh

# Verify MCP server
python scripts/verify_mcp_server.py
```

## Script Requirements

### macOS-Specific Scripts
- `start-dev.sh` - Uses `osascript` for Terminal

### General Requirements
- `bash` - All scripts
- `python3` + `venv` - Backend scripts
- `node` + `npm` - Frontend scripts
- `docker` - Docker-related benchmarks (optional)

## Environment Variables

Scripts respect these environment variables:

```bash
# Use production environment
ENVIRONMENT=production ./scripts/start-backend.sh

# Custom ports
PORT=3000 ./scripts/start-frontend.sh
API_PORT=9000 ./scripts/start-backend.sh
```

## Exit Codes

Scripts follow standard exit code conventions:
- `0` - Success
- `1` - General error
- `2` - Misuse (wrong arguments)
- `127` - Command not found

## Adding New Scripts

1. Create script in `scripts/` directory
2. Make executable: `chmod +x scripts/your-script.sh`
3. Add shebang: `#!/bin/bash`
4. Add description comment at top
5. Document in this README
6. Test on clean environment

### Script Template

```bash
#!/bin/bash
# Description: What this script does
# Usage: ./scripts/my-script.sh [options]

set -e  # Exit on error

# Script implementation
echo "Starting..."

# Success
echo "✅ Done!"
exit 0
```

## Troubleshooting

### Permission Denied
```bash
chmod +x scripts/script-name.sh
```

### Script Not Found
```bash
# Run from project root
./scripts/script-name.sh

# NOT from scripts directory
cd scripts && ./script-name.sh  # ❌ May break relative paths
```

### macOS Terminal Errors
```bash
# If osascript fails, enable Terminal in System Preferences:
# System Preferences → Security & Privacy → Automation
# Allow Terminal to control Terminal
```

### Virtual Environment Not Found
```bash
# Backend scripts need venv
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Integration with Makefile

Most scripts have Makefile aliases (from project root):

```bash
make dev          # ./scripts/start-dev.sh
make backend      # ./scripts/start-backend.sh
make frontend     # ./scripts/start-frontend.sh
make test         # Comprehensive tests
make test-fast    # ./scripts/quick-test.sh
make benchmark    # ./scripts/benchmark.sh
```

See [Makefile](../Makefile) for complete list.

## Performance Notes

Scripts are optimized for M3 Max hardware but work on any system:
- Benchmark results scale with CPU cores
- Parallel testing adapts to available cores
- ThreadPoolExecutor dynamically sizes workers

## Contributing

When adding/modifying scripts:
1. Follow existing naming convention (`action-description.sh`)
2. Add comprehensive comments
3. Update this README
4. Test on clean environment
5. Add Makefile alias if appropriate
6. Use `set -e` for error handling
7. Provide user feedback (echo statements)
8. Exit with appropriate code

## Resources

- [Bash Best Practices](https://bertvv.github.io/cheat-sheets/Bash.html)
- [ShellCheck](https://www.shellcheck.net/) - Shell script linter
- [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html)
