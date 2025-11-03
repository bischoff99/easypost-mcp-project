Organize project files and clean cache (M3 Max optimized with 16 parallel workers).

**Context-aware**: Analyzes current project structure and applies intelligent organization based on `.dev-config.json` conventions.

## What It Cleans

**File Organization:**
- Move misplaced test files to `{{paths.tests}}`
- Move services to `{{paths.services}}`
- Move models to `{{paths.models}}`
- Move utilities to `{{paths.utils}}`
- Organize components to `{{paths.components}}`

**Cache Cleanup (Parallel):**
- Python: `__pycache__/`, `*.pyc`, `.pytest_cache/`
- JavaScript: `node_modules/.cache/`, `.vite/`, `dist/`
- Go: Binary files, `*.test`
- Rust: `target/debug/`, `target/release/`
- General: `.DS_Store`, `Thumbs.db`, temp files

**Code Quality:**
- Remove unused imports (ruff --fix, eslint --fix)
- Fix formatting issues (black, prettier)
- Update .gitignore with cache patterns
- Remove empty directories

## MCP Integration

**Stage 1 - Scan** (Desktop Commander):
- Action: `list_directory` with depth=3
- Identifies: Misplaced files, cache directories
- Time: 1-2s

**Stage 2 - Parallel Cache Cleanup** (Desktop Commander):
- Action: `start_search` for cache files
- Parallel: 16 workers via `xargs -P 16`
- Delete: Using `mdfind` on macOS for 10x faster search
- Time: 2-5s for 1000+ files

**Stage 3 - File Organization** (Desktop Commander):
- Action: `move_file` for each misplaced file
- Follows: `{{paths.*}}` patterns from config
- Creates: Missing directories automatically
- Time: 1-3s

**Stage 4 - Import Cleanup** (Desktop Commander):
- Python: `ruff check --select F401,F841 --fix`
- JavaScript: `eslint --fix --rule 'no-unused-vars: error'`
- Parallel: Process multiple files simultaneously
- Time: 2-5s

**Stage 5 - Verification**:
- Runs: Tests to ensure nothing broke
- Checks: All imports still resolve
- Reports: Files moved, cache cleaned

## Auto-Detection

Detects project type from:

**Python Project:**
- Indicators: `requirements.txt`, `pyproject.toml`, `.py` files
- Cleans: `__pycache__/`, `*.pyc`, `.pytest_cache/`, `.mypy_cache/`
- Organizes: By convention (snake_case files)

**JavaScript Project:**
- Indicators: `package.json`, `.js/.jsx/.ts/.tsx` files
- Cleans: `node_modules/.cache/`, `dist/`, `.vite/`, `.next/`
- Organizes: By convention (PascalCase components, camelCase utils)

**Go Project:**
- Indicators: `go.mod`, `.go` files
- Cleans: Binary files, `*.test`, build artifacts
- Organizes: By Go conventions

**Multi-Language Project:**
- Detects: All languages present
- Cleans: All cache types
- Organizes: Respects each language's conventions

## File Organization Rules

**From .dev-config.json:**
```json
{
  "paths": {
    "tests": "backend/tests",
    "services": "backend/src/services",
    "models": "backend/src/models",
    "components": "frontend/src/components"
  },
  "conventions": {
    "python": {
      "files": "snake_case.py"
    },
    "javascript": {
      "files": "PascalCase.jsx"
    }
  }
}
```

**Applied automatically:**
- `test_user.py` → `backend/tests/unit/test_user.py`
- `UserCard.jsx` → `frontend/src/components/UserCard.jsx`
- `user_service.py` → `backend/src/services/user_service.py`

## Performance (M3 Max)

**Parallel Operations:**
- Cache file search: Uses `mdfind` (macOS Spotlight) - 10x faster
- File deletion: `xargs -P 16` - 16 parallel workers
- Import cleanup: Process multiple files simultaneously
- Total speedup: 5-10x vs sequential

**Metrics:**
```
🧹 Cleaning project with 16 parallel workers...

Cache cleanup:
- Found: 1,247 cache files
- Deleted: 1,247 files in 2.3s
- Workers: 16
- Speedup: 8.2x

File organization:
- Scanned: 543 files
- Moved: 12 misplaced files
- Time: 1.8s

Import cleanup:
- Python: Fixed 5 unused imports
- JavaScript: Fixed 3 unused imports
- Time: 3.2s

✅ Cleanup complete in 7.3s
```

## Safety Features

- **Dry-run mode**: Shows what will be done without doing it
- **Backup**: Creates snapshot before moving files
- **Verification**: Runs tests after organization
- **Rollback**: Can undo if something breaks
- **Gitignore**: Only cleans files that should be ignored

## Usage Examples

```bash
# Default - clean entire project
/clean

# Specific directory
/clean backend/src/

# Dry-run to preview
/clean --dry-run

# Cache only (no file moves)
/clean --cache-only

# Files only (no cache cleanup)
/clean --organize-only
```

## Output Format

```
🧹 Project Cleanup (M3 Max: 16 workers)

📊 Scan Results:
- Project type: Python + JavaScript (auto-detected)
- Cache files: 1,247 found
- Misplaced files: 12 found
- Unused imports: 8 found

🚀 Cleaning (parallel)...

✅ Cache Cleanup (2.3s):
- __pycache__/: 156 directories
- *.pyc: 891 files
- node_modules/.cache/: 200 files
- Speedup: 8.2x (16 workers)

✅ File Organization (1.8s):
- test_bulk_tools.py → backend/tests/unit/
- UserCard.jsx → frontend/src/components/
- 10 more files moved

✅ Import Cleanup (3.2s):
- Python: ruff fixed 5 unused imports
- JavaScript: eslint fixed 3 unused vars

🧪 Verification:
- Tests: ✅ 45/45 passed
- Imports: ✅ All resolve

✅ Cleanup complete in 7.3s
- Files moved: 12
- Cache cleaned: 1,247 files
- Imports fixed: 8
```

## Adapts To Any Project

**Reads from .dev-config.json:**
- File paths: Where to move files
- Conventions: Naming patterns to detect
- Language: Which cache types to clean
- Test command: How to verify changes

**Works with:**
- Python, JavaScript, TypeScript, Go, Rust, Ruby, Java
- Any project structure
- Any naming convention
- Any test framework

## What It Doesn't Do

**Safe by default:**
- ❌ Never deletes source code
- ❌ Never modifies git history
- ❌ Never touches node_modules/ (except .cache)
- ❌ Never removes files tracked by git
- ✅ Only cleans gitignored files
- ✅ Only moves files to standard locations
- ✅ Always creates backups

**One command. Clean project. Any stack.**

