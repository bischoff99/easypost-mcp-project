# REST Client Extension Setup (FREE)

## REST Client by Huachao Mao
**Extension ID:** `humao.rest-client`
**Status:** ✅ FREE (Open Source)
**Alternative to:** Thunder Client, Postman

## Installation

1. Open Cursor IDE
2. Press `Cmd+Shift+X` (Mac) or `Ctrl+Shift+X` (Windows/Linux)
3. Search for "REST Client"
4. Install "REST Client" by Huachao Mao

## Configuration

✅ Already configured in:
- `.vscode/settings.json` - Environment variables
- `api-requests.http` - Request file with examples

## Usage

### 1. Switch Environment
- Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
- Type: "Rest Client: Switch Environment"
- Select: `development` or `production`

### 2. Make Requests
- Open `api-requests.http` file
- Click "Send Request" above any request
- Or use shortcut: `Cmd+Alt+R` (Mac) / `Ctrl+Alt+R` (Windows/Linux)

### 3. View Response
- Response appears in a new tab
- Can save responses
- Supports variables: `{{baseUrl}}`, `{{apiUrl}}`, etc.

## Environments

### Development
- Base URL: `http://localhost:8000`
- API Key: Test key (EZTK...)
- Use for: Local development

### Production
- Base URL: `http://localhost:80`
- API URL: `http://localhost:80/api`
- API Key: Production key (EZAK...)
- Use for: Docker production

## Features

✅ **FREE** - No account required
✅ **Lightweight** - No external app needed
✅ **Integrated** - Works directly in Cursor IDE
✅ **Variables** - Environment variable support
✅ **History** - Request history tracking
✅ **GraphQL** - Supports GraphQL queries
✅ **cURL** - Can generate cURL commands

## Example Request

```http
### Health Check
GET {{baseUrl}}/health
Accept: application/json
```

## Files

- `api-requests.http` - Main request file (20+ examples)
- `.vscode/settings.json` - Environment configuration
- `.cursor/REST_API_ENVIRONMENTS.md` - Full documentation

## Comparison

| Feature | REST Client | Thunder Client |
|---------|-------------|----------------|
| **Price** | ✅ FREE | ✅ FREE |
| **Account** | ❌ Not needed | ❌ Not needed |
| **File Format** | `.http` files | JSON collections |
| **Integration** | ✅ Native | ✅ Native |
| **Variables** | ✅ Yes | ✅ Yes |
| **History** | ✅ Yes | ✅ Yes |

**Recommendation:** REST Client is simpler and file-based (easier to version control).
