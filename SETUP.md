# Project Setup Commands

## Quick Setup

```bash
# 1. Clone repository (if not already cloned)
git clone <repository-url>
cd easypost-mcp-project

# 2. Setup environment variables
cp .env.example .env
# Edit .env with your EasyPost API key

# 3. Setup direnv (auto-loads .env)
direnv allow

# 4. Setup backend
cd backend
python3 -m venv venv
source venv/bin/activate  # or let direnv do this automatically
pip install -r requirements.txt

# 5. Setup frontend
cd ../frontend
npm install

# 6. Start development servers
# Terminal 1 - Backend
cd backend
uvicorn src.server:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

## One-Line Setup (if direnv is configured)

```bash
cd /Users/andrejs/Developer/github/andrejs/easypost-mcp-project && \
cp .env.example .env && \
direnv allow && \
cd backend && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && \
cd ../frontend && npm install
```

## Environment Variables

After copying `.env.example` to `.env`, edit `.env` and set:
- `EASYPOST_API_KEY` - Your EasyPost API key (get from https://easypost.com/account/api-keys)
- `DATABASE_URL` - PostgreSQL connection string (if using database)

## Verify Setup

```bash
# Check backend
cd backend
python -c "from src.utils.config import settings; print(f'API Key: {settings.EASYPOST_API_KEY[:10]}...')"

# Check frontend
cd frontend
npm run build
```

## Start Development

```bash
# Backend (http://localhost:8000)
cd backend
uvicorn src.server:app --reload

# Frontend (http://localhost:5173)
cd frontend
npm run dev
```
