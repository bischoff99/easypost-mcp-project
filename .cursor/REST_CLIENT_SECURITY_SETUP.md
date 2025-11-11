# REST Client Security Setup Guide

**Last Updated**: November 11, 2025
**Security Review**: docs/reviews/REST_ENVIRONMENT_SECURITY_REVIEW_2025.md

---

## 🚨 IMPORTANT: Security First

**NEVER commit API keys or credentials!**

This guide ensures secure REST client configuration without exposing secrets.

---

## 🔒 Secure Setup (5 minutes)

### Step 1: Copy Template Files

```bash
# REST Client configuration
cp .cursor/rest-client-environments.json.example .cursor/rest-client-environments.json

# Thunder Client configuration
cp .thunder-client/thunder-environment.json.example .thunder-client/thunder-environment.json
```

### Step 2: Verify .env File

Ensure your `.env` file contains:

```bash
# Required for REST clients
EASYPOST_API_KEY=EZTK_your_test_key_here
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/easypost_mcp
```

### Step 3: Verify Configuration

The configuration files now use environment variable references:

```json
{
  "development": {
    "easypostApiKey": "${EASYPOST_API_KEY}",  // ✅ Reads from .env
    "databaseUrl": "${DATABASE_URL}"           // ✅ Reads from .env
  }
}
```

### Step 4: Test REST Client

1. Open `docs/api-requests.http`
2. Switch environment: `Cmd+Shift+P` → "Rest Client: Switch Environment" → Development
3. Click "Send Request" on Health Check
4. Should see ✅ 200 OK response

---

## 🛡️ Security Checklist

Before using REST clients:

- [ ] Copied .example templates to actual files
- [ ] Never edited .example files directly
- [ ] Verified .env contains required keys
- [ ] Confirmed .gitignore includes config files
- [ ] Tested requests work with env vars
- [ ] Never committed actual config files

---

## 📁 File Status

### ✅ Safe to Commit (IN GIT)

These files are templates without secrets:

- `.cursor/rest-client-environments.json.example`
- `.thunder-client/thunder-environment.json.example`
- `docs/api-requests.http`
- `.cursor/REST_CLIENT_SETUP.md`
- `.cursor/REST_CLIENT_SECURITY_SETUP.md` (this file)

### ❌ NEVER Commit (LOCAL ONLY)

These files contain your actual API keys:

- `.cursor/rest-client-environments.json` (gitignored)
- `.thunder-client/thunder-environment.json` (gitignored)
- `.env` (gitignored)

---

## 🔑 Environment Variables Reference

### Required Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `EASYPOST_API_KEY` | EasyPost API authentication | `EZTK151720...` (test) |
| `DATABASE_URL` | PostgreSQL connection | `postgresql://...` |

### Optional Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `MCP_HOST` | Server host | `0.0.0.0` |
| `MCP_PORT` | Server port | `8000` |
| `CORS_ORIGINS` | Allowed origins | `http://localhost:5173` |

---

## 🚀 Using REST Clients

### REST Client (Huachao Mao)

**Extension ID**: `humao.rest-client`

**Usage**:
1. Open `docs/api-requests.http`
2. `Cmd+Shift+P` → "Rest Client: Switch Environment"
3. Select "development" or "production"
4. Click "Send Request" above any request
5. View response in new tab

**Variables**:
- `{{baseUrl}}` - Base server URL
- `{{apiUrl}}` - API endpoint URL
- `{{easypostApiKey}}` - EasyPost API key (from .env)

### Thunder Client

**Extension ID**: `rangav.vscode-thunder-client`

**Usage**:
1. Open Thunder Client sidebar (⚡ icon)
2. Click "Env" tab
3. Select "Development" or "Production"
4. Click request from collection or create new
5. View response in Thunder Client panel

**Variables**:
- `{{baseUrl}}` - Base server URL
- `{{apiUrl}}` - API endpoint URL
- `{{easypostApiKey}}` - EasyPost API key (from .env)

---

## ⚠️ Troubleshooting

### Variables Not Resolving

**Problem**: Requests show `${EASYPOST_API_KEY}` literally

**Solution**:
1. Check `.env` file exists in project root
2. Verify variable name matches exactly
3. Restart VS Code/Cursor
4. Check REST Client extension is installed

### 401 Unauthorized Errors

**Problem**: API returns 401 status

**Solution**:
1. Verify `.env` has correct API key
2. Check key format: Test keys start with `EZTK`, production with `EZAK`
3. Ensure key is not expired
4. Test key validity: https://easypost.com/account/api-keys

### Environment Not Switching

**Problem**: Wrong environment selected

**Solution**:
1. REST Client: `Cmd+Shift+P` → "Rest Client: Switch Environment"
2. Thunder Client: Click "Env" tab, select environment
3. Check bottom status bar for active environment

---

## 🔐 Security Best Practices

### DO's ✅

1. **Use Template Files**
   ```bash
   cp .example .actual
   ```

2. **Reference Environment Variables**
   ```json
   "apiKey": "${API_KEY}"
   ```

3. **Keep Secrets in .env**
   ```bash
   # .env (gitignored)
   API_KEY=actual_key_here
   ```

4. **Rotate Keys Regularly**
   - Test keys: Every 6 months
   - Production keys: Every 90 days

### DON'Ts ❌

1. **Never Hardcode Secrets**
   ```json
   "apiKey": "EZTK..."  // ❌ NEVER!
   ```

2. **Never Commit .env**
   ```bash
   git add .env  // ❌ NEVER!
   ```

3. **Never Share Keys in Chat/Email**
   ```
   Slack: "Here's the key: EZTK..."  // ❌ NEVER!
   ```

4. **Never Use Production Keys in Development**
   ```bash
   EASYPOST_API_KEY=EZAK_prod_key  // ❌ NEVER in dev!
   ```

---

## 📚 Additional Resources

### REST Client Extension
- Marketplace: https://marketplace.visualstudio.com/items?itemName=humao.rest-client
- Documentation: https://github.com/Huachao/vscode-restclient
- dotenv support: Built-in with `{{$dotenv VAR}}`

### Thunder Client
- Marketplace: https://marketplace.visualstudio.com/items?itemName=rangav.vscode-thunder-client
- Documentation: https://www.thunderclient.com/docs
- Environment variables: `{{process.env.VAR}}`

### Security Tools
- **detect-secrets**: Prevent committing secrets
- **git-secrets**: AWS secret detection
- **BFG Repo Cleaner**: Remove secrets from history

---

## 🎯 Quick Reference

### Setup Checklist

1. ✅ Copy .example files to actual files
2. ✅ Verify .env has required variables
3. ✅ Confirm .gitignore includes config files
4. ✅ Test request with health check
5. ✅ Never commit actual config files

### File Locations

- **Requests**: `docs/api-requests.http`
- **REST Client Config**: `.cursor/rest-client-environments.json` (gitignored)
- **Thunder Config**: `.thunder-client/thunder-environment.json` (gitignored)
- **Templates**: `*.example` files (in git)
- **Secrets**: `.env` (gitignored)

### Common Commands

```bash
# Copy templates
make rest-setup  # (if added to Makefile)

# Or manually
cp .cursor/rest-client-environments.json.example .cursor/rest-client-environments.json
```

---

**Maintained By**: EasyPost MCP Team
**Security Review**: November 11, 2025
**Next Review**: February 11, 2026 (quarterly)

**Related Docs**:
- Security Review: `docs/reviews/REST_ENVIRONMENT_SECURITY_REVIEW_2025.md`
- Setup Guide: `.cursor/REST_CLIENT_SETUP.md`
- API Environments: `.cursor/REST_API_ENVIRONMENTS.md`
