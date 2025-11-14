# MCP Environment Switching Guide

## Overview

This guide explains how to work with test and production EasyPost API keys during MCP server development.

## The Challenge

When developing MCP servers that wrap 3rd party APIs like EasyPost:
- You need to test tools without burning production credits
- MCP servers start fresh on each invocation
- No interactive environment to switch keys at runtime
- Need clear separation between test and production

## Solution: Dual MCP Server Configuration

We use **two separate MCP server configurations** in `.cursor/mcp.json`:
- `easypost-test`: Test environment (safe for development, EZTK key)
- `easypost-prod`: Production environment (explicit, for real shipments, EZAK key)

## Configuration Files

### Environment-Specific Files

**`apps/backend/.env.test`** (Development/Testing)
```bash
EASYPOST_API_KEY=EZTK...your_test_key_here
ENVIRONMENT=test
MCP_LOG_LEVEL=DEBUG
DATABASE_URL=postgresql+asyncpg://easypost:easypost@localhost:5432/easypost_mcp_test
```

**`apps/backend/.env.production`** (Production/Live)
```bash
EASYPOST_API_KEY=EZAK...your_production_key_here
ENVIRONMENT=production
MCP_LOG_LEVEL=INFO
DATABASE_URL=postgresql+asyncpg://easypost:easypost@localhost:5432/easypost_mcp
```

### Cursor MCP Configuration

**`.cursor/mcp.json`**
```json
{
  "version": "2.1.0",
  "mcpServers": {
    "easypost-test": {
      "command": "/full/path/to/venv/bin/python",
      "args": ["/full/path/to/run_mcp.py"],
      "cwd": "/full/path/to/backend",
      "env": {
        "ENVIRONMENT": "test"
      }
    },
    "easypost-prod": {
      "command": "/full/path/to/venv/bin/python",
      "args": ["/full/path/to/run_mcp.py"],
      "cwd": "/full/path/to/backend",
      "env": {
        "ENVIRONMENT": "production"
      }
    }
  }
}
```

## Daily Workflow

### Phase 1: Development (Test API Only)

During tool development and testing:

```bash
# Terminal: Unit tests
cd apps/backend
ENVIRONMENT=test pytest tests/ -v

# VS Code: Select "Python: Backend Server (Test)" from debug menu
# Or press F5 and choose the test configuration
```

**In Cursor IDE:**
- Use `easypost-test` MCP server (test environment)
- All tool invocations use test API key
- No production charges
- Safe to experiment

```
Cursor Chat:
"Create a test shipment to London"
→ Uses easypost-test MCP server → EZTK test key → no real charge
```

### Phase 2: Production Validation

When you need to test real shipments:

**In Cursor IDE:**
- Explicitly use `easypost-prod` server
- Real charges will apply
- Production warnings logged

```
Cursor Chat:
"Use easypost-prod to create a shipment to New York"
→ Uses easypost-prod MCP server → EZAK prod key → real charge
```

## VS Code/Cursor Debug Configurations

Launch configurations available (press F5):

### Backend Server
- **"Python: Backend Server (Test)"** - Test API, DEBUG logging
- **"Python: Backend Server (Production)"** - Production API, INFO logging

### MCP Server
- **"Python: MCP Server (Test)"** - Test environment
- **"Python: MCP Server (Production)"** - Production environment

### Full Stack
- **"Full Stack Debug (Test)"** - Backend (test) + Frontend
- **"Full Stack Debug (Production)"** - Backend (prod) + Frontend

## Safety Features

### Environment Detection

The MCP server automatically detects and logs its environment on startup:

**Test Mode:**
```
✓ MCP Server running in TEST mode
✓ Using API key: EZTK...
```

**Production Mode:**
```
⚠️  MCP SERVER RUNNING IN PRODUCTION MODE - Real API calls will be made!
⚠️  Using API key: EZAK...
```

### Tool-Level Warnings

Critical MCP tools log warnings in production mode:

```python
# create_shipment
⚠️  PRODUCTION MODE: Creating real shipments with actual charges!

# buy_shipment_label  
⚠️  PRODUCTION MODE: Purchasing real shipping labels with actual charges!

# refund_shipment
⚠️  PRODUCTION MODE: Refunding real shipments!
```

## Verification Commands

### Check Test Environment
```bash
cd apps/backend
ENVIRONMENT=test python -c "from src.mcp_server import mcp; from src.utils.config import settings; print(f'Server: {mcp.name}'); print(f'Environment: {settings.ENVIRONMENT}'); print(f'API Key: {settings.EASYPOST_API_KEY[:4]}...')"
```

Expected output:
```
✓ MCP Server running in TEST mode
Server: EasyPost Shipping Server (TEST)
Environment: test
API Key: EZTK...
```

### Check Production Environment
```bash
cd apps/backend
ENVIRONMENT=production python -c "from src.mcp_server import mcp; from src.utils.config import settings; print(f'Server: {mcp.name}'); print(f'Environment: {settings.ENVIRONMENT}'); print(f'API Key: {settings.EASYPOST_API_KEY[:4]}...')"
```

Expected output:
```
⚠️  MCP SERVER RUNNING IN PRODUCTION MODE - Real API calls will be made!
Server: EasyPost Shipping Server (PRODUCTION)
Environment: production
API Key: EZAK...
```

## Troubleshooting

### Wrong API Key Being Used

**Problem:** Test environment using production key (EZAK instead of EZTK)

**Solution:**
1. Check `.env.test` has correct test key
2. Verify `ENVIRONMENT=test` is set when running
3. Restart Cursor to reload MCP configuration

### MCP Server Not Switching Environments

**Problem:** Both servers use same environment

**Solution:**
1. Check `.cursor/mcp.json` has correct `env` settings
2. Restart Cursor completely (not just reload)
3. Verify environment files exist: `.env.test` and `.env.production`

### Production Warnings Not Showing

**Problem:** No warnings when using production

**Solution:**
Check MCP server initialization - warnings added to `src/mcp_server/__init__.py`

## Best Practices


1. **Default to Test**
   - Always use `easypost-test` server during development
   - Only use `easypost-prod` when explicitly needed

2. **Visual Confirmation**
   - Check MCP server name in Cursor: "(TEST)" or "(PRODUCTION)"
   - Look for warning symbols (⚠️) in production

3. **Protect Production**
   - Never set production as default
   - Always require explicit selection for production
   - Review logs before production operations

4. **Environment Variables**
   - Don't set `EASYPOST_API_KEY` in main `.env` file
   - Let environment-specific files control keys
   - Use `ENVIRONMENT` variable to switch contexts

5. **Testing Strategy**
   - Unit tests: Always use test environment
   - Integration tests: Use test API exclusively
   - Production validation: Minimal, explicit operations only

## File Structure Summary

```
project/
├── .cursor/
│   └── mcp.json                    # Dual server configuration
├── apps/backend/
│   ├── .env                        # Shared config (no API keys)
│   ├── .env.test                   # Test API key (EZTK...)
│   ├── .env.production             # Production API key (EZAK...)
│   └── src/
│       └── mcp_server/
│           ├── __init__.py         # Environment detection
│           └── tools/              # Tool-level warnings
└── .vscode/
    └── launch.json                 # Debug configs for both environments
```

## Quick Reference

| Action | Command/Selection |
|--------|-------------------|
| **MCP Development** | Use `easypost-test` server in Cursor |
| **Production Test** | Use `easypost-prod` server in Cursor |
| **Backend Dev** | Select "Backend Server (Test)" in VS Code |
| **Backend Prod** | Select "Backend Server (Production)" in VS Code |
| **Unit Tests** | `ENVIRONMENT=test pytest tests/` |
| **Verify Test** | Check for "EZTK" in API key |
| **Verify Production** | Check for "EZAK" in API key + warnings |

## Related Documentation

- [MCP Tools Usage](./MCP_TOOLS_USAGE.md) - MCP tool documentation
- [Environment Setup](../setup/ENVIRONMENT_SETUP.md) - Initial configuration
- [Quick Reference](./QUICK_REFERENCE.md) - Code templates and patterns

## Support

If you encounter issues:
1. Check this guide's troubleshooting section
2. Verify environment files are correctly configured
3. Restart Cursor completely
4. Check logs for environment detection messages
