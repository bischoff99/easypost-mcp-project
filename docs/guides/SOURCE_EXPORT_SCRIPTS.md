# Source Code Export Scripts

**Location:** `scripts/export_backend_source.sh`, `scripts/export_frontend_source.sh`  
**Status:** ✅ Ready to Use

---

## Overview

Export clean source code archives of backend and frontend applications. Creates timestamped zip files to avoid overwriting previous exports.

---

## Features

### Backend Export (`export_backend_source.sh`)
- Exports `apps/backend/src/` directory
- Excludes build artifacts, caches, tests, and dependencies
- Creates timestamped zip: `backend_src_YYYYMMDD_HHMMSS.zip`

### Frontend Export (`export_frontend_source.sh`)
- Exports `apps/frontend/src/` directory
- Excludes node_modules, build artifacts, and test files
- Creates timestamped zip: `frontend_src_YYYYMMDD_HHMMSS.zip`

---

## Usage

### Via Makefile (Recommended)
```bash
make export-backend   # Export backend source
make export-frontend # Export frontend source
```

### Direct Script Execution
```bash
zsh scripts/export_backend_source.sh
zsh scripts/export_frontend_source.sh
```

### Via Cursor Commands
In Cursor Command Palette (Cmd+Shift+P):
- Run Command → `/export-backend`
- Run Command → `/export-frontend`

---

## Excluded Files

### Backend Export Excludes
- `__pycache__/` directories
- `*.pyc`, `*.pyo` compiled files
- `venv/`, `.venv/` virtual environments
- `tests/` directory
- `*.log`, `*.tmp`, `*.bak` temporary files
- `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`
- `htmlcov/`, `.coverage` coverage files
- `dist/`, `build/` build artifacts

### Frontend Export Excludes
- `node_modules/` directory
- `dist/`, `build/` build directories
- `.next/`, `.vite/` framework caches
- `*.log`, `*.tmp`, `*.bak` temporary files
- `*.test.js`, `*.test.jsx`, `*.spec.js`, `*.spec.jsx` test files
- `.svelte-kit/`, `.nuxt/`, `.cache/` framework-specific caches
- `coverage/` test coverage

---

## Output

### File Naming
- **Backend:** `backend_src_20251111_051500.zip`
- **Frontend:** `frontend_src_20251111_051500.zip`

### Location
- All archives created in project root directory

### Example Output
```
🧩 Exporting backend source from /path/to/apps/backend → backend_src_20251111_051500.zip
✅ Backend archive created at: backend_src_20251111_051500.zip
   backend_src_20251111_051500.zip → 2.3M
```

---

## Integration

### Makefile
```makefile
export-backend:
	@zsh scripts/export_backend_source.sh

export-frontend:
	@zsh scripts/export_frontend_source.sh
```

### Cursor Universal Commands
Commands are registered in `.cursor/config/universal-commands.json`:
- `/export-backend` - Export backend source
- `/export-frontend` - Export frontend source

---

## Use Cases

1. **Code Sharing:** Share clean source code without dependencies
2. **Backup:** Create source code backups before major changes
3. **Deployment:** Prepare source archives for deployment
4. **Code Review:** Share code for review without build artifacts
5. **Archive:** Create historical snapshots of source code

---

## Notes

- **Read-only:** Scripts never modify source files
- **Safe:** Can be run repeatedly without side effects
- **Timestamped:** Each export creates a unique file
- **Clean:** Only includes source code, excludes all artifacts
- **Fast:** Uses native `zip` command for efficiency

---

**Status:** ✅ Production-ready and integrated into project workflow

