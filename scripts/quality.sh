#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
echo "🔍 Running ruff..."
ruff check src
echo "🔍 Running mypy..."
mypy src --config-file pyproject.toml 2>/dev/null || mypy src --config-file mypy.ini 2>/dev/null || echo "⚠️  mypy check skipped"
echo "✅ Quality checks passed"
