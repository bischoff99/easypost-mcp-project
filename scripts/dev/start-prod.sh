#!/usr/bin/env zsh
# Production startup script for EasyPost MCP (backend only)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${(%):-%x}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
VENV_BIN="${PROJECT_ROOT}/venv/bin"
LOG_DIR="${PROJECT_ROOT}/logs"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

info() { echo -e "${BLUE}ℹ${NC} $1"; }
success() { echo -e "${GREEN}✓${NC} $1"; }
warning() { echo -e "${YELLOW}⚠${NC} $1"; }
error() { echo -e "${RED}✗${NC} $1"; }

cleanup() {
    info "Shutting down backend..."
    kill 0 2>/dev/null || true
    exit 0
}

trap cleanup EXIT INT TERM

if [ ! -f "${VENV_BIN}/python" ]; then
    error "Virtual environment not found. Run 'make setup' first."
    exit 1
fi

if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    warning "Port 8000 already in use, stopping existing process..."
    pkill -f "uvicorn.*src.server" || true
    sleep 2
fi

info "Loading environment variables..."
if [ -f "${PROJECT_ROOT}/config/.env" ]; then
    set -a
    source "${PROJECT_ROOT}/config/.env"
    set +a
fi

if [ -z "${EASYPOST_API_KEY:-}" ]; then
    warning "EASYPOST_API_KEY not set. Ensure production key is configured."
fi

mkdir -p "${LOG_DIR}"

WORKERS=${WORKERS:-4}
export ENVIRONMENT=production
export DEBUG=false
export LOG_LEVEL=INFO

info "Starting backend (workers=${WORKERS})..."
cd "${PROJECT_ROOT}"
"${VENV_BIN}/python" -m uvicorn src.server:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers "${WORKERS}" \
    --loop uvloop \
    --log-level info \
    --proxy-headers \
    > "${LOG_DIR}/production.log" 2>&1 &

BACKEND_PID=$!
info "Backend PID: ${BACKEND_PID}"

info "Waiting for health check..."
for i in {1..30}; do
    if curl -s http://localhost:8000/health >/dev/null 2>&1; then
        success "Backend ready at http://localhost:8000"
        break
    fi
    if [ $i -eq 30 ]; then
        error "Backend failed to start"
        kill $BACKEND_PID 2>/dev/null || true
        exit 1
    fi
    sleep 1
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
success "Production backend running!"
echo ""
echo "  URL:      http://localhost:8000"
echo "  Docs:     http://localhost:8000/docs"
echo "  Workers:  ${WORKERS}"
echo ""
echo "  Logs: tail -f ${LOG_DIR}/production.log"
echo "  Stop: Ctrl+C"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

wait
