# REST API Client Configurations

## Supported Extensions

### 1. REST Client (Huachao Mao)
**Extension ID:** `humao.rest-client`

**Configuration:**
- `.vscode/settings.json` - Environment variables
- `api-requests.http` - HTTP request file

**Usage:**
1. Open `api-requests.http`
2. Switch environment: `Ctrl+Shift+P` → "Rest Client: Switch Environment"
3. Click "Send Request" above any request

**Environments:**
- `development` - Test API key, localhost:8000
- `production` - Production API key, localhost:80/api

### 2. Thunder Client
**Extension ID:** `rangav.vscode-thunder-client`

**Configuration:**
- `.vscode/settings.json` - Thunder Client settings
- `.thunder-client/thunder-environment.json` - Environment backup

**Usage:**
1. Open Thunder Client sidebar (Thunder icon)
2. Click "Environments" tab
3. Select "Development" or "Production"
4. Use collection requests or create new ones

**Environments:**
- `Development` - Test API key, localhost:8000
- `Production` - Production API key, localhost:80/api

## Environment Variables

🚨 **SECURITY**: See [REST_CLIENT_SECURITY_SETUP.md](./REST_CLIENT_SECURITY_SETUP.md) for secure configuration

### Development (Secure Pattern)
```json
{
  "baseUrl": "http://localhost:8000",
  "apiUrl": "http://localhost:8000",
  "frontendUrl": "http://localhost:5173",
  "easypostApiKey": "${EASYPOST_API_KEY}",
  "databaseUrl": "${DATABASE_URL}",
  "environment": "development"
}
```

### Production (Secure Pattern)
```json
{
  "baseUrl": "http://localhost:80",
  "apiUrl": "http://localhost:80/api",
  "frontendUrl": "http://localhost:80",
  "easypostApiKey": "${EASYPOST_API_KEY}",
  "databaseUrl": "${DATABASE_URL}",
  "environment": "production"
}
```

**Important**: Values are read from `.env` file (gitignored). See templates:
- `.cursor/rest-client-environments.json.example`
- `.thunder-client/thunder-environment.json.example`

## Quick Reference

### REST Client (.http files)
- Variables: `{{baseUrl}}`, `{{apiUrl}}`, `{{easypostApiKey}}`
- Switch: Command Palette → "Rest Client: Switch Environment"
- Send: Click "Send Request" or `Ctrl+Alt+R`

### Thunder Client
- Variables: `{{baseUrl}}`, `{{apiUrl}}`, `{{easypostApiKey}}`
- Switch: Thunder sidebar → Environments → Select environment
- Send: Click request in collection

## Files Created

- `.vscode/settings.json` - Settings for both extensions
- `api-requests.http` - REST Client request file
- `.thunder-client/thunder-environment.json` - Thunder Client environment backup
- `.cursor/rest-client-environments.json` - Environment variables reference
- `.cursor/REST_API_ENVIRONMENTS.md` - This documentation
