#!/bin/bash

echo "🚀 Starting EasyPost MCP Development Environment"
echo "=============================================="
echo ""

# Terminal 1: Backend
echo "Starting Backend Server (Terminal 1)..."
osascript -e 'tell application "Terminal"
    do script "cd /Users/andrejs/Developer/github/andrejs/easypost-mcp-project/backend && source venv/bin/activate && echo \"🐍 Backend Server Starting...\" && uvicorn src.server:app --reload --log-level warning"
end tell'

sleep 2

# Terminal 2: Frontend
echo "Starting Frontend Server (Terminal 2)..."
osascript -e 'tell application "Terminal"
    do script "cd /Users/andrejs/Developer/github/andrejs/easypost-mcp-project/frontend && echo \"⚛️  Frontend Server Starting...\" && npm run dev"
end tell'

echo ""
echo "✅ Development servers starting in separate terminals"
echo ""
echo "📍 URLs:"
echo "   Backend API:  http://localhost:8000"
echo "   API Docs:     http://localhost:8000/docs"
echo "   Frontend:     http://localhost:5173"
echo ""
echo "🧪 Test endpoints:"
echo "   curl http://localhost:8000/health"
echo "   curl http://localhost:8000/api/recent-shipments"
echo ""
