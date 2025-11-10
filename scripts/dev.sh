#!/bin/bash
set -e

echo "🚀 Starting EasyPost development servers..."

# Function to cleanup on exit
cleanup() {
  echo ""
  echo "🛑 Shutting down servers..."
  kill 0
}
trap cleanup EXIT

# Start backend in background
echo "📦 Starting backend server..."
(
  cd backend
  if [ -f ./.venv/bin/uvicorn ]; then
    echo "   Backend: http://localhost:8000"
    ./.venv/bin/uvicorn src.server:app --host 0.0.0.0 --port 8000 --reload --log-level warning 2>&1 | sed 's/^/   [Backend] /'
  else
    echo "❌ Backend venv not set up. Run: cd backend && uv venv .venv && uv pip install -r requirements.txt"
    sleep 1000000
  fi
) &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 2

# Start frontend
echo "⚡ Starting frontend server..."
(
  cd frontend
  echo "   Frontend: http://localhost:5173"
  npm run dev 2>&1 | sed 's/^/   [Frontend] /'
) &
FRONTEND_PID=$!

echo ""
echo "✅ Both servers running!"
echo "   Backend:  http://localhost:8000"
echo "   Frontend: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop all servers"
echo ""

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
