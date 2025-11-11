# Project Normalization Script

**Safe, reversible project structure normalization for EasyPost MCP**

## Overview

Converts the current project structure to a standardized monorepo layout:
- `backend/` → `apps/backend/`
- `frontend/` → `apps/frontend/`
- `docker/` → `deploy/`
- Creates `packages/core/` for shared code

## Safety Features

- ✅ **Automatic backup** before any changes
- ✅ **rsync-based moves** (preserves timestamps, ownership)
- ✅ **Reversible** - generates undo script automatically
- ✅ **Idempotent** - safe to run multiple times
- ✅ **Non-destructive** - only moves files, never deletes source code

## Usage

```bash
# Run normalization
bash scripts/normalize_project.sh

# Review changes
git status

# Test build
make dev

# If needed, undo
bash scripts/undo_normalize.sh
```

## What It Does

### Directory Moves

| From | To | Status |
|------|-----|--------|
| `backend/` | `apps/backend/` | ✅ Safe move |
| `frontend/` | `apps/frontend/` | ✅ Safe move |
| `docker/` | `deploy/` | ✅ Safe move |

### File Updates

- ✅ Updates `Makefile` paths
- ✅ Updates Docker Compose paths
- ✅ Updates `.cursor/config.json`
- ✅ Updates `scripts/shell-integration.sh`

### New Structure Created

```
apps/
├── backend/
│   └── src/          # Backend source code
└── frontend/
    └── src/          # Frontend source code

packages/
└── core/
    ├── py/           # Shared Python code
    └── ts/           # Shared TypeScript code

deploy/
├── docker-compose.yml
└── docker-compose.prod.yml

tests/
└── e2e/              # E2E tests
```

## Backup & Undo

### Automatic Backup

Before any changes, the script creates a backup:
```
.normalize_backup_YYYYMMDD_HHMMSS/
├── backend/
├── frontend/
├── docker/
├── Makefile
└── ...
```

### Undo Script

An undo script is automatically generated:
```bash
bash scripts/undo_normalize.sh
```

This restores:
- Original directory structure
- Original file paths
- Original configurations

## Pre-Normalization Checklist

Before running, ensure:
- ✅ All changes committed or stashed
- ✅ No running Docker containers
- ✅ Backend/frontend servers stopped
- ✅ Git repository clean

## Post-Normalization Steps

1. **Review changes:**
   ```bash
   git status
   git diff
   ```

2. **Test build:**
   ```bash
   make dev
   ```

3. **Update any hardcoded paths:**
   - CI/CD configurations
   - Documentation
   - IDE settings

4. **Commit:**
   ```bash
   git add -A
   git commit -m "chore: normalize project structure to monorepo layout"
   ```

## Troubleshooting

### Script Fails Mid-Execution

The script uses `rsync --remove-source-files`, which only removes source files after successful copy. If interrupted:
- Partial moves remain intact
- Re-run the script (it's idempotent)
- Or use undo script to restore

### Path Issues After Normalization

If paths are broken:
1. Check `Makefile` - paths should be `apps/backend/` and `apps/frontend/`
2. Check Docker Compose files - paths should be `../apps/backend`
3. Check shell integration - paths should be updated
4. Run undo script if needed: `bash scripts/undo_normalize.sh`

### Docker Compose Errors

If Docker Compose fails:
```bash
# Check paths in docker-compose files
grep -r "backend\|frontend" deploy/

# Should show:
#   - ../apps/backend
#   - ../apps/frontend
```

## Comparison

### Before Normalization

```
easypost-mcp-project/
├── backend/
├── frontend/
├── docker/
└── scripts/
```

### After Normalization

```
easypost-mcp-project/
├── apps/
│   ├── backend/
│   └── frontend/
├── packages/
│   └── core/
├── deploy/
└── scripts/
```

## Benefits

1. **Standard monorepo structure** - matches industry patterns
2. **Better organization** - clear separation of apps vs packages
3. **Scalability** - easy to add more apps/packages
4. **Tool compatibility** - works with Turborepo, Nx, etc.

## Reversibility

The normalization is fully reversible:
- Backup created automatically
- Undo script generated
- Original structure can be restored

## Related Scripts

- `scripts/clean_project_parallel.sh` - Cleanup after normalization
- `scripts/undo_normalize.sh` - Reverse normalization (auto-generated)

