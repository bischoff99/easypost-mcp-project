# Setup Instructions

## Backend Setup

1. Navigate to backend directory:
```bash
cd /Users/andrejs/easypost-mcp-project/backend
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
- Open `.env` file
- Replace `your_easypost_api_key_here` with your actual EasyPost API key

5. Make startup script executable and run:
```bash
chmod +x start_backend.sh
./start_backend.sh
```

Backend will run on: http://localhost:8000

## MCP Notes

The legacy React UI has been removed. The backend doubles as the MCP server and optional HTTP API:

- Use Claude Desktop (MCP) or REST clients to interact with the system.
- Swagger docs remain available at http://localhost:8000/docs for manual testing.

## Testing

Visit http://localhost:8000/health to verify backend is running.
Use `python scripts/python/mcp_tool.py list_tools` to confirm MCP registration.

## Project Structure

```
easypost-mcp-project/
├── backend/
│   ├── src/
│   │   ├── services/
│   │   │   └── easypost_service.py
│   │   ├── utils/
│   │   │   └── config.py
│   │   └── server.py
│   ├── requirements.txt
│   ├── .env
│   └── start_backend.sh
└── scripts/
    ├── dev/
    ├── test/
    └── python/
```
