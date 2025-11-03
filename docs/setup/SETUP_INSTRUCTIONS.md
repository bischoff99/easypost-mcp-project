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

## Frontend Setup

1. Navigate to frontend directory (in a new terminal):
```bash
cd /Users/andrejs/easypost-mcp-project/frontend
```

2. Install dependencies:
```bash
npm install
```

3. Make startup script executable and run:
```bash
chmod +x start_frontend.sh
./start_frontend.sh
```

Frontend will run on: http://localhost:5173

## Testing

Visit http://localhost:8000/health to verify backend is running
Visit http://localhost:5173 to access the dashboard

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
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── Dashboard.jsx
    │   │   └── Dashboard.css
    │   ├── services/
    │   │   └── api.js
    │   ├── App.jsx
    │   └── main.jsx
    ├── package.json
    └── start_frontend.sh
```
