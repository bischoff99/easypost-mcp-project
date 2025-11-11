# Full Repository Review Script

**Location:** `scripts/full_repo_review.py`  
**Status:** ✅ Enhanced and Production-Ready

---

## Overview

Comprehensive repository analysis tool that performs deep structural and configuration audits of the EasyPost MCP monorepo.

---

## Features

### 1. Repository Statistics
- Total file count
- Total lines of code
- Code files/lines (excluding binaries)
- Language breakdown by extension
- Largest files identification

### 2. Structure Verification
- Critical path checks (`apps/backend/src/server.py`, `apps/frontend/src/App.jsx`, etc.)
- Directory structure validation
- Docker Compose configuration validation

### 3. Dependency Analysis
- Python dependencies from `requirements.txt`
- Node dependencies from `package.json`
- Dependency count summary

### 4. Security Scanning
- Detects secrets/API keys in `.env` files
- Excludes `.env.example` files
- Warns about potential security issues

### 5. Duplicate Detection
- File hash-based duplicate detection
- Filters out expected duplicates (empty files, placeholders)
- Excludes binary files from analysis

### 6. Docker Audit
- Validates Docker Compose configuration
- Checks for required services (backend, frontend, postgres)

---

## Usage

### Basic Review
```bash
python3 scripts/full_repo_review.py
```

### JSON Output (for CI/CD)
```bash
python3 scripts/full_repo_review.py --json > repo_report.json
```

### Via Makefile
```bash
make review          # Human-readable output
make review-json     # JSON output saved to docs/reviews/
```

---

## Output Format

### Human-Readable Output
- Repository statistics
- Language breakdown
- Largest files
- Critical file checks
- Docker validation
- Security warnings
- Duplicate file detection
- Dependency summaries

### JSON Output
```json
{
  "summary": {
    ".py": {"files": 157, "lines": 34026},
    ...
  },
  "results": {
    "missing": [],
    "docker_issues": [],
    "env_secrets": [...],
    "duplicates": {...},
    "python_deps": [...],
    "node_deps": [...]
  },
  "largest": [
    ["path/to/file", size_in_bytes],
    ...
  ]
}
```

---

## Ignored Directories

The script automatically excludes:
- `node_modules/`
- `__pycache__/`
- `.venv/`, `venv/`
- `.cursor/`
- `.git/`
- `.normalize_backup*/`
- `.pytest_cache/`, `.ruff_cache/`, `.mypy_cache/`
- `htmlcov/`, `coverage/`, `dist/`, `build/`
- `.next/`, `.vite/`

---

## Enhancements Made

### 1. Better Filtering
- Excludes backup directories from analysis
- Skips binary files in duplicate detection
- Filters out empty placeholder files

### 2. Improved Output
- Separate code file/lines statistics
- Cleaner duplicate reporting
- Better formatted warnings

### 3. Enhanced Security
- Excludes `.env.example` from secret scanning
- Better error handling for file reads
- More accurate secret detection

### 4. Performance
- Skips entire directory trees early
- Efficient file walking
- Minimal memory footprint

---

## Example Output

```
📁 Repository Root: /path/to/repo
Total files: 783
Total lines: 174,217
Code files (excluding binaries): 721
Code lines (excluding binaries): 166,332

📊 Languages / File Extensions:
       .md:   236 files,    73956 lines
       .py:   157 files,    34026 lines
     .json:    32 files,    24616 lines
      .jsx:   115 files,    15699 lines
      ...

✅ All critical files present
✅ Docker configuration valid
📦 Python Dependencies: 23 packages
📦 Node Dependencies: 38 packages
```

---

## Integration

### CI/CD Integration
```yaml
# GitHub Actions example
- name: Repository Review
  run: |
    python3 scripts/full_repo_review.py --json > review.json
    # Process JSON output for CI checks
```

### Pre-commit Hook
```bash
#!/bin/bash
python3 scripts/full_repo_review.py
if [ $? -ne 0 ]; then
    echo "Repository review failed"
    exit 1
fi
```

---

## Exit Codes

- `0` - Review completed successfully
- `1` - Error during review (file access issues, etc.)

---

## Notes

- **Read-only:** Script never modifies repository files
- **Safe:** Can be run at any time without side effects
- **Fast:** Optimized for large repositories
- **Accurate:** Excludes build artifacts and dependencies

---

**Status:** ✅ Production-ready and integrated into project workflow

