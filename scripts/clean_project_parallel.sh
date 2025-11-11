#!/usr/bin/env zsh
#
# Parallel cleanup for EasyPost MCP workspace
# Optimized for multi-core Apple Silicon (M3 Max: 16 cores)
# Usage: zsh scripts/clean_project_parallel.sh [--deep]
# Uses zsh for better macOS compatibility
#

set -euo pipefail
# zsh equivalent: setopt extendedglob
setopt extendedglob

# Detect CPU cores (M3 Max = 16 logical cores)
JOBS=$(sysctl -n hw.logicalcpu 2>/dev/null || nproc 2>/dev/null || echo 8)
DEEP=${1:-""}

echo "🧹 Parallel cleanup using $JOBS threads..."

# --- helpers ------------------------------------------------------------

run_parallel() {
  # Read list of paths from stdin, delete in parallel
  xargs -P "$JOBS" -I {} rm -rf "{}" 2>/dev/null || true
}

# --- Docker cleanup -----------------------------------------------------

echo "→ Stopping Docker containers..."
docker compose -f deploy/docker-compose.yml down -v --remove-orphans >/dev/null 2>&1 || true
docker compose -f deploy/docker-compose.prod.yml down -v --remove-orphans >/dev/null 2>&1 || true

# --- Python artifacts ---------------------------------------------------

echo "→ Cleaning Python caches..."

# Parallel directory deletion
find apps/backend -type d \( \
  -name "__pycache__" \
  -o -name ".pytest_cache" \
  -o -name ".mypy_cache" \
  -o -name ".ruff_cache" \
  -o -name "htmlcov" \
  -o -name "*.egg-info" \
\) 2>/dev/null | run_parallel

# Parallel file deletion
find apps/backend -type f \( \
  -name "*.pyc" \
  -o -name "*.pyo" \
  -o -name ".coverage" \
  -o -name "coverage.json" \
\) -print0 2>/dev/null | xargs -0 -P "$JOBS" rm -f 2>/dev/null || true

# Single operations (already fast)
rm -rf apps/backend/{build,dist,*.egg-info} 2>/dev/null || true

# --- Node artifacts -----------------------------------------------------

echo "→ Cleaning Node/build directories..."

# Parallel directory deletion
find apps/frontend -type d \( \
  -name "node_modules" \
  -o -name "dist" \
  -o -name ".vite" \
  -o -name "coverage" \
  -o -name ".turbo" \
\) 2>/dev/null | run_parallel

# Single operations
rm -rf apps/frontend/{.next,.vercel,*.log} 2>/dev/null || true

# --- Cursor cache -------------------------------------------------------

echo "→ Cleaning Cursor cache..."
rm -rf .cursor/{index,cache,archive} 2>/dev/null || true

# --- Docker system cache ------------------------------------------------

echo "→ Cleaning Docker build cache..."
docker builder prune -f >/dev/null 2>&1 || true
docker volume prune -f >/dev/null 2>&1 || true

# --- Logs and temporary files ------------------------------------------

echo "→ Cleaning logs and temporary files..."
find . -type f \( \
  -name "*.log" \
  -o -name "*.swp" \
  -o -name "*.swo" \
  -o -name "*~" \
\) -print0 2>/dev/null | xargs -0 -P "$JOBS" rm -f 2>/dev/null || true

# --- Deep mode ----------------------------------------------------------

if [[ "$DEEP" == "--deep" ]]; then
  echo "⚠️  Deep clean: pruning images + developer caches..."
  
  docker system prune -a -f >/dev/null 2>&1 || true
  
  echo "→ Removing user-level caches..."
  
  # Parallel user cache deletion
  printf "%s\n" \
    "$HOME/.cache/pip" \
    "$HOME/.npm" \
    "$HOME/.pnpm-store" \
    "$HOME/.cache/pytest" \
    "$HOME/.cache/mypy" \
    "$HOME/.cache/ruff" \
    "$HOME/.cache/starship" \
    2>/dev/null | run_parallel
  
  # Clean Python user caches
  python3 -m pip cache purge 2>/dev/null || true
  
  # Clean npm cache
  npm cache clean --force 2>/dev/null || true
fi

# --- Recreate essentials ------------------------------------------------

mkdir -p apps/backend/venv apps/frontend/node_modules .cursor/index 2>/dev/null || true

# --- Summary ------------------------------------------------------------

echo "✅ Cleanup complete."

# Show repo size (if du is available)
if command -v du >/dev/null 2>&1; then
  du -sh . 2>/dev/null | awk '{print "Repo size after cleanup:", $1}' || true
fi

if [[ "$DEEP" == "--deep" ]]; then
  echo "💡 Deep clean completed. Use without '--deep' for standard cleanup."
else
  echo "💡 Use '--deep' flag for full cache + image purge."
fi

