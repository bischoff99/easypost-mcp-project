# 🔧 Environment Configuration Guide

**Status:** ✅ Configured  
**Standard:** 12-Factor App with `.env` files  
**Date:** November 3, 2025

---

## 📁 Environment Files

### **Backend (Python/FastAPI)**
```
backend/
├── .env                    ← Local dev (gitignored) - DEFAULT
├── .env.development        ← Dev defaults (committed) - TEST KEY
├── .env.production         ← Production (gitignored) - LIVE KEY
└── .env.example            ← Template (committed)
```

### **Frontend (React/Vite)**
```
frontend/
├── .env                    ← Local dev (gitignored)
├── .env.development        ← Dev defaults (committed)
├── .env.production         ← Production (committed)
└── .env.example            ← Template (committed)
```

---

## 🔑 API Keys Configured

### **Development (Test Mode)**
- **File:** `backend/.env.development`
- **Key:** `EZTK...` (EasyPost Test Key)
- **Safe to commit:** ✅ Yes (test key)
- **Use for:** Local development, testing

### **Production (Live Mode)**
- **File:** `backend/.env.production`
- **Key:** `your_production_api_key_here...` (EasyPost Production Key)
- **Safe to commit:** ❌ NO - Gitignored
- **Use for:** Production deployments only

---

## 🚀 Quick Start

### **Development (Default)**
```bash
# Option 1: Automated (Recommended)
Cmd+Shift+P → "Run Task" → "🚀 Dev: Full Stack"

# Option 2: Manual
cd backend && source venv/bin/activate && uvicorn src.server:app --reload
cd frontend && npm run dev
```

Uses: `backend/.env` (test key) + `frontend/.env.development`

### **Production Mode**
```bash
# Option 1: Tasks
Cmd+Shift+P → "Run Task" → "🏭 Prod: Backend"

# Option 2: Manual
cd backend && ENVIRONMENT=production uvicorn src.server:app
cd frontend && npm run build && npm run preview
```

Uses: `backend/.env.production` (live key) + `frontend/.env.production`

---

## 🎯 How It Works

### **Backend Auto-Loading**
The `config.py` automatically loads the correct environment:

```python
# Reads ENVIRONMENT variable (default: development)
ENVIRONMENT=development → Loads .env.development (test key)
ENVIRONMENT=production → Loads .env.production (live key)
```

### **Frontend Auto-Loading**
Vite automatically loads based on command:

```bash
npm run dev     → Loads .env.development
npm run build   → Loads .env.production
```

---

## 🔄 Switching Environments

### **Method 1: VS Code Tasks (Keyboard Shortcut)**
1. Press `Cmd+Shift+P`
2. Type "Run Task"
3. Select environment:
   - `🚀 Dev: Full Stack` (test key)
   - `🏭 Prod: Backend` (live key)
   - `🐳 Docker: Start` (production)

### **Method 2: Environment Variable**
```bash
# Development
ENVIRONMENT=development uvicorn src.server:app --reload

# Production
ENVIRONMENT=production uvicorn src.server:app
```

### **Method 3: Docker Compose**
```bash
# Uses .env.production automatically
docker compose up --build
```

---

## ✅ What's Gitignored

**Ignored (Secrets):**
- `.env` (local overrides)
- `.env.production` (live keys)
- `.env.local`
- `backend/.env`
- `backend/.env.production`
- `frontend/.env`

**Committed (Safe):**
- `.env.example` (template)
- `.env.development` (test keys)
- `backend/.env.development`
- `frontend/.env.development`
- `frontend/.env.production` (no secrets)

---

## 🛡️ Security Best Practices

### ✅ DO:
- Use test keys (EZTK) for development
- Keep production keys (your_production_api_key_here) in `.env.production`
- Commit `.env.development` (test keys are safe)
- Use platform secrets for cloud deployment

### ❌ DON'T:
- Commit `.env.production` (has live key)
- Hardcode API keys in source code
- Share production keys in chat/email
- Use production keys locally

---

## 📊 Environment Comparison

| Aspect | Development | Production |
|--------|------------|------------|
| **API Key** | EZTK (test) | your_production_api_key_here (live) |
| **File** | `.env.development` | `.env.production` |
| **Committed** | ✅ Yes | ❌ No |
| **Backend URL** | localhost:8000 | Your domain |
| **Debug Mode** | ON | OFF |
| **Log Level** | DEBUG | WARNING |
| **Hot Reload** | ✅ Yes | ❌ No |

---

## 🧪 Testing Configuration

### **Verify Development Setup**
```bash
cd backend && source venv/bin/activate
python -c "from src.utils.config import settings; print(f'Key: {settings.EASYPOST_API_KEY[:10]}...')"
# Should show: EZTK151720...
```

### **Verify Production Setup**
```bash
cd backend && ENVIRONMENT=production python -c "from src.utils.config import settings; print(f'Key: {settings.EASYPOST_API_KEY[:10]}...')"
# Should show: your_production_api_key_here...
```

---

## 🚨 Troubleshooting

### **Problem: "EASYPOST_API_KEY is required"**
**Solution:** Create `backend/.env` file:
```bash
cp backend/.env.development backend/.env
```

### **Problem: Using wrong API key**
**Solution:** Check environment:
```bash
echo $ENVIRONMENT  # Should be 'development' or 'production'
```

### **Problem: Frontend can't connect to backend**
**Solution:** Verify `VITE_API_URL` in `frontend/.env.development`:
```bash
VITE_API_URL=http://localhost:8000
```

---

## 📚 Additional Resources

- **12-Factor App:** https://12factor.net/config
- **Vite Env:** https://vitejs.dev/guide/env-and-mode.html
- **python-dotenv:** https://github.com/theskumar/python-dotenv
- **EasyPost Docs:** https://easypost.com/docs

---

**Questions?** Check `DEV_DEPLOYMENT_GUIDE.md` for detailed setup instructions.
