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

## Maintenance Scripts

### `cleanup-codebase.sh`
Comprehensive codebase cleanup and optimization.

```bash
./scripts/cleanup-codebase.sh
```

**What it does:**
- Removes Python caches (`__pycache__`, `.pyc`)
- Cleans test artifacts (`.pytest_cache`, `htmlcov`)
- Removes build outputs (`dist/`, `build/`)
- Cleans node_modules cache (`.vite`)
- Formats code (black, prettier)
- Runs linters (ruff, eslint)
- Shows disk space saved

**Warning:** Removes cached files (safe operation)

---

### `cleanup-unused-code.sh`
Detect and optionally remove unused code.

```bash
./scripts/cleanup-unused-code.sh
```

**What it does:**
- Finds unused Python imports (via autoflake)
- Detects unused React components
- Identifies commented code blocks
- Finds empty files
- Generates report of findings

**Requirements:** macOS (uses `mdfind` for Spotlight search)
**Note:** Review findings before deleting

---

### `optimize-structure.sh`
Optimize project structure and organization.

```bash
./scripts/optimize-structure.sh
```

**What it does:**
- Analyzes directory structure
- Suggests improvements
- Optionally reorganizes files
- Updates imports after moves

**Warning:** May move files - commit changes first

---

### `verify-structure.sh`
Verify project structure integrity.

```bash
./scripts/verify-structure.sh
```

**What it does:**
- Checks required directories exist
- Verifies configuration files
- Validates imports
- Checks for broken links in docs
- Generates structure report

**Output:** Pass/fail report with recommendations

---

## Setup Scripts

### `setup-pnpm.sh`
Install and configure pnpm package manager.

```bash
./scripts/setup-pnpm.sh
```

**What it does:**
- Installs pnpm globally
- Configures pnpm for project
- Migrates from npm if needed
- Faster installs and better disk usage

---

### `setup-uv.sh`
Install and configure uv (fast Python package installer).

```bash
./scripts/setup-uv.sh
```

**What it does:**
- Installs uv package manager
- Configures for faster pip installs
- 10-100x faster than pip

---

### `install-universal-commands.sh`
Install universal slash commands system.

```bash
./scripts/install-universal-commands.sh
```

**What it does:**
- Installs `.cursor/commands/` structure
- Copies universal command templates
- Sets up command aliases
- Configures for project

---

### `create-dev-toolkit-repo.sh`
Create a portable dev toolkit repository.

```bash
./scripts/create-dev-toolkit-repo.sh
```

**What it does:**
- Packages scripts for reuse
- Creates standalone toolkit repo
- Includes documentation
- Useful for sharing across projects

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

### Maintenance Workflow
```bash
# Clean before commit
./scripts/cleanup-codebase.sh

# Verify structure
./scripts/verify-structure.sh

# Find unused code
./scripts/cleanup-unused-code.sh
```

## Script Requirements

### macOS-Specific Scripts
- `start-dev.sh` - Uses `osascript` for Terminal
- `cleanup-unused-code.sh` - Uses `mdfind` for Spotlight

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
make clean        # ./scripts/cleanup-codebase.sh
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
