#!/usr/bin/env zsh
# macOS Terminal windows startup script
# Usage: ./scripts/dev/start-dev.sh

set -euo pipefail

# Get project root (two levels up from scripts/dev/)
PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
BACKEND_DIR="${PROJECT_ROOT}"
VENV_DIR="${PROJECT_ROOT}/venv"

echo "🚀 Starting EasyPost MCP Development Environment"
echo "=============================================="
echo ""

# Detect venv location
if [ -d "${VENV_DIR}" ]; then
    VENV_PATH="${VENV_DIR}"
else
    echo "❌ Error: Virtual environment not found. Run 'make setup' first."
    exit 1
fi

# Terminal 1: Backend
echo "Starting Backend Server (Terminal 1)..."
osascript -e "tell application \"Terminal\"
    do script \"cd '${BACKEND_DIR}' && source '${VENV_PATH}/bin/activate' && echo '🐍 Backend Server Starting...' && uvicorn src.server:app --reload --log-level warning\"
end tell"

sleep 2

echo ""
echo "✅ Backend server starting in new terminal"
echo ""
echo "📍 URLs:"
echo "   Backend API:  http://localhost:8000"
echo "   API Docs:     http://localhost:8000/docs"
echo ""
echo "🧪 Test endpoints:"
echo "   curl http://localhost:8000/health"
echo "   curl http://localhost:8000/api/recent-shipments"
echo ""
