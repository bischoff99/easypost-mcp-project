# EasyPost MCP Project

Production-ready EasyPost shipping integration with MCP server and React frontend.

## Quick Start

### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Add your EasyPost API key to .env
./start_backend.sh
```

### Frontend
```bash
cd frontend
npm install
./start_frontend.sh
```

## URLs
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- Health: http://localhost:8000/health

## Features
✅ CORS configured
✅ Error handling
✅ Async/await
✅ Input validation
✅ Logging
