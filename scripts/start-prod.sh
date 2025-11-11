#!/bin/bash
# Production startup script for EasyPost MCP
# Builds frontend and starts both servers in production mode

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Project root is one level up from scripts directory
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
BACKEND_DIR="${PROJECT_ROOT}/backend"
FRONTEND_DIR="${PROJECT_ROOT}/frontend"

# Colours for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Colour

# Function to print coloured output
info() { echo -e "${BLUE}ℹ${NC} $1"; }
success() { echo -e "${GREEN}✓${NC} $1"; }
warning() { echo -e "${YELLOW}⚠${NC} $1"; }
error() { echo -e "${RED}✗${NC} $1"; }

# Check if virtual environment exists
if [ ! -f "${BACKEND_DIR}/venv/bin/python" ]; then
    error "Backend virtual environment not found!"
    error "Run: cd apps/backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Check if node_modules exists
if [ ! -d "${FRONTEND_DIR}/node_modules" ]; then
    warning "Frontend dependencies not installed. Installing..."
    cd "${FRONTEND_DIR}" && npm install
fi

# Check for port conflicts
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    warning "Port 8000 is already in use. Stopping existing processes..."
    pkill -f "uvicorn.*src.server" || true
    sleep 2
fi

if lsof -Pi :4173 -sTCP:LISTEN -t >/dev/null 2>&1; then
    warning "Port 4173 is already in use. Stopping existing processes..."
    pkill -f "vite preview" || true
    sleep 2
fi

# Check environment variables
if [ -z "${EASYPOST_API_KEY}" ]; then
    warning "EASYPOST_API_KEY not set. Using .env file if available."
fi

# Build frontend
info "Building frontend for production..."
cd "${FRONTEND_DIR}"
if npm run build; then
    success "Frontend build complete!"
else
    error "Frontend build failed!"
    exit 1
fi

# Check if dist directory exists
if [ ! -d "${FRONTEND_DIR}/dist" ]; then
    error "Frontend dist directory not found after build!"
    exit 1
fi

# Function to cleanup on exit
cleanup() {
    info "Shutting down production servers..."
    kill 0 2>/dev/null || true
    exit 0
}

trap cleanup EXIT INT TERM

# Start backend in production mode
info "Starting backend in production mode..."

# Production settings
export ENVIRONMENT=production
export DEBUG=false
export LOG_LEVEL=INFO
export WORKERS=${WORKERS:-4}  # Default to 4 workers, can override

# Ensure we're using the venv Python
if [ ! -f "${BACKEND_DIR}/venv/bin/python" ]; then
    error "Virtual environment Python not found at ${BACKEND_DIR}/venv/bin/python"
    exit 1
fi

# Ensure logs directory exists
mkdir -p "${BACKEND_DIR}/logs"

# Load environment variables from .env if it exists
if [ -f "${BACKEND_DIR}/.env" ]; then
    set -a
    source "${BACKEND_DIR}/.env"
    set +a
fi

# Start backend with production settings
cd "${BACKEND_DIR}"
"${BACKEND_DIR}/venv/bin/python" -m uvicorn src.server:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers "${WORKERS}" \
    --loop uvloop \
    --log-level info \
    --no-access-log \
    --proxy-headers \
    > "${BACKEND_DIR}/logs/production.log" 2>&1 &

BACKEND_PID=$!
info "Backend started (PID: ${BACKEND_PID}) on http://localhost:8000"

# Wait for backend to be ready
info "Waiting for backend to be ready..."
for i in {1..30}; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        success "Backend is ready!"
        break
    fi
    if [ $i -eq 30 ]; then
        error "Backend failed to start after 30 seconds"
        kill $BACKEND_PID 2>/dev/null || true
        exit 1
    fi
    sleep 1
done

# Start frontend preview server
info "Starting frontend preview server..."
cd "${FRONTEND_DIR}"

# Use vite preview if available, otherwise use serve
if command -v vite >/dev/null 2>&1 || [ -f "${FRONTEND_DIR}/node_modules/.bin/vite" ]; then
    "${FRONTEND_DIR}/node_modules/.bin/vite" preview \
        --host 0.0.0.0 \
        --port 4173 \
        --outDir dist \
        > "${FRONTEND_DIR}/logs/production.log" 2>&1 &
else
    # Fallback to serve if vite preview not available
    if command -v serve >/dev/null 2>&1; then
        serve -s dist -l 4173 > "${FRONTEND_DIR}/logs/production.log" 2>&1 &
    else
        warning "Neither vite preview nor serve found. Installing serve..."
        npx -y serve -s dist -l 4173 > "${FRONTEND_DIR}/logs/production.log" 2>&1 &
    fi
fi

FRONTEND_PID=$!
info "Frontend started (PID: ${FRONTEND_PID}) on http://localhost:4173"

# Wait for frontend to be ready
info "Waiting for frontend to be ready..."
sleep 3

# Display status
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
success "Production servers running!"
echo ""
echo "  Backend:  http://localhost:8000"
echo "  Frontend: http://localhost:4173"
echo "  API Docs: http://localhost:8000/docs"
echo ""
echo "  Backend PID:  ${BACKEND_PID}"
echo "  Frontend PID: ${FRONTEND_PID}"
echo "  Workers:      ${WORKERS}"
echo ""
echo "  Logs:"
echo "    Backend:  tail -f ${BACKEND_DIR}/logs/production.log"
echo "    Frontend: tail -f ${FRONTEND_DIR}/logs/production.log"
echo ""
echo "  Press Ctrl+C to stop all servers"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Create logs directory if it doesn't exist
mkdir -p "${FRONTEND_DIR}/logs"

# Keep script running
wait
