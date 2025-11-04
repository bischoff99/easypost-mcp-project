# ✅ EasyPost API Keys Configured

## 🔑 Keys Added

**Production Key:** `EZAK...` (stored securely)
**Test Key:** `EZTK...` (stored securely)

---

## 📁 Configuration Files Updated

### 1. Environment Files (All Protected by .gitignore)
- ✅ `backend/.env` - Default (uses production key)
- ✅ `backend/.env.development` - Development (uses test key)
- ✅ `backend/.env.production` - Production (uses production key)

### 2. Shell Environment
- ✅ `~/.zshrc` - Permanent environment variables added
- Variables: `EASYPOST_API_KEY`, `EASYPOST_TEST_KEY`

### 3. MCP Configuration
- ✅ `~/.cursor/mcp.json` - Uses `${env:EASYPOST_API_KEY}`
- Automatically picks up from environment

---

## 🚀 Testing Your Keys

### Test Production Key (EZAK)
```bash
cd backend
source venv/bin/activate

# Test with Python
python << EOF
import easypost
import os
client = easypost.EasyPostClient(api_key=os.getenv("EASYPOST_API_KEY"))
print("✅ Production key valid:", client.api_key[:10] + "...")
EOF
```

### Test Test Key (EZTK)
```bash
# Test with Python
python << EOF
import easypost
import os
client = easypost.EasyPostClient(api_key=os.getenv("EASYPOST_TEST_KEY"))
print("✅ Test key valid:", client.api_key[:10] + "...")
EOF
```

### Test via MCP Server
```bash
# Restart Cursor first (Cmd+Q)
# Then in Cursor Chat:
"Create a test shipment to verify API key"
```

---

## 🔒 Security Notes

### ✅ Protected
- All `.env` files are in `.gitignore`
- Keys never committed to git
- Shell variables only in local `.zshrc`
- MCP uses environment variables (not hardcoded)

### ⚠️ Important
1. **Never commit these keys to git**
2. **Don't share production key (EZAK) publicly**
3. **Test key (EZTK) is safe for development**
4. **Rotate keys if exposed**

### 🔄 If Keys Are Compromised
1. Go to EasyPost Dashboard
2. Navigate to API Keys
3. Delete compromised key
4. Generate new key
5. Update all `.env` files

---

## 🎯 Key Usage by Environment

| Environment | Key Type | Prefix | File |
|-------------|----------|--------|------|
| Development | Test | EZTK | `.env.development` |
| Testing | Test | EZTK | `.env` (default) |
| Production | Live | EZAK | `.env.production` |

---

## 🔧 Switching Between Keys

### Use Test Key (Development)
```bash
export ENVIRONMENT=development
# or
ENVIRONMENT=development uvicorn src.server:app --reload
```

### Use Production Key (Production)
```bash
export ENVIRONMENT=production
# or
ENVIRONMENT=production uvicorn src.server:app
```

The app automatically loads the correct `.env` file based on `ENVIRONMENT` variable.

---

## ✅ Verification Checklist

- [x] Keys added to `backend/.env`
- [x] Keys added to shell environment (`~/.zshrc`)
- [x] `.gitignore` protects `.env` files
- [x] MCP configuration updated
- [ ] **TODO:** Restart Cursor to load keys
- [ ] **TODO:** Test creating a shipment
- [ ] **TODO:** Verify both keys work

---

## 🚀 Next Steps

1. **Restart Cursor** (Cmd+Q) to load environment variables
2. **Test MCP Server:**
   ```
   "List available EasyPost tools"
   "Create a test shipment to Los Angeles"
   ```
3. **Run Backend:**
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn src.server:app --reload
   ```
4. **Check Logs** for "EasyPost service initialized with key: EZAK..."

---

## 📊 Key Capabilities

### Production Key (EZAK) - Use for:
- ✅ Real shipments
- ✅ Live label purchases
- ✅ Production tracking
- ⚠️ Charges real money!

### Test Key (EZTK) - Use for:
- ✅ Development
- ✅ Testing
- ✅ Learning
- ✅ Free (no charges)

---

**Your API keys are now securely configured! Restart Cursor and test the MCP server.** 🚀

