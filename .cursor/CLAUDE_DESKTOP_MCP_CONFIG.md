# Claude Desktop MCP Configuration

## Overview

This guide shows how to integrate the EasyPost MCP Server with Claude Desktop, enabling Claude to create shipments, track packages, and get shipping rates directly.

## Configuration File Location

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

## Current Claude Desktop Config

Your current config has these MCP servers:
- `sequential-thinking`
- `clear-thought-mcp`
- `exa`
- `mcpsemanticscholar`

## Add EasyPost MCP Server

### Step 1: Backup Current Config

```bash
cp ~/Library/Application\ Support/Claude/claude_desktop_config.json \
   ~/Library/Application\ Support/Claude/claude_desktop_config.json.backup
```

### Step 2: Edit Configuration

Open the config file:

```bash
open ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

### Step 3: Add EasyPost Server

Add this entry to the `mcpServers` object:

```json
{
  "preferences": {
    "quickEntryDictationShortcut": "capslock"
  },
  "mcpServers": {
    "easypost-shipping": {
      "command": "/Users/andrejs/easypost-mcp-project/backend/venv/bin/python",
      "args": [
        "/Users/andrejs/easypost-mcp-project/backend/run_mcp.py"
      ],
      "env": {
        "EASYPOST_API_KEY": "EZTK151720b5bbc44c08bd3c3f7a055b69acOSQagEFWUPCil26sR0flew",
        "PYTHONPATH": "/Users/andrejs/easypost-mcp-project/backend"
      }
    },
    "sequential-thinking": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-sequential-thinking"
      ]
    },
    "clear-thought-mcp": {
      "command": "npx",
      "args": [
        "-y",
        "@smithery/cli@latest",
        "run",
        "@ThinkFar/clear-thought-mcp",
        "--key",
        "42a5f315-6698-4388-9265-bc61d3d6cde9"
      ]
    },
    "exa": {
      "command": "npx",
      "args": [
        "-y",
        "@smithery/cli@latest",
        "run",
        "exa",
        "--key",
        "42a5f315-6698-4388-9265-bc61d3d6cde9",
        "--profile",
        "female-reindeer-HxQXa2"
      ]
    },
    "mcpsemanticscholar": {
      "command": "npx",
      "args": [
        "-y",
        "@smithery/cli@latest",
        "run",
        "@hamid-vakilzadeh/mcpsemanticscholar",
        "--key",
        "42a5f315-6698-4388-9265-bc61d3d6cde9",
        "--profile",
        "female-reindeer-HxQXa2"
      ]
    }
  }
}
```

**Important**: Place `easypost-shipping` at the top of the `mcpServers` list for easy access.

### Configuration Explained

```json
"easypost-shipping": {
  "command": "/path/to/venv/bin/python",    // Python 3.12 from virtual environment
  "args": ["/path/to/run_mcp.py"],          // MCP server runner script
  "env": {
    "EASYPOST_API_KEY": "YOUR_KEY",         // EasyPost API key
    "PYTHONPATH": "/path/to/backend"        // Python module path
  }
}
```

## Step 4: Restart Claude Desktop

After saving the config:
1. **Quit Claude Desktop completely** (Cmd+Q)
2. **Reopen Claude Desktop**
3. The EasyPost MCP server will initialize automatically

## Step 5: Verify Integration

In Claude Desktop, type:

```
What MCP tools do you have available?
```

You should see:
- ✅ `create_shipment` - Create a new shipment and purchase a label
- ✅ `get_tracking` - Get real-time tracking information
- ✅ `get_rates` - Get available shipping rates

## Using the EasyPost MCP Tools

### Create a Shipment

```
Create a shipment from:
- John Smith, 456 Oak Ave, New York, NY 10001

To:
- Jane Doe, 123 Main St, San Francisco, CA 94102

Package: 10x8x5 inches, 2 pounds
Carrier: USPS
```

### Track a Package

```
Track shipment with tracking number: EZ1000000001
```

### Get Shipping Rates

```
Get shipping rates for a 10x8x5 inch, 2 pound package from New York to San Francisco
```

## Troubleshooting

### Server Not Loading

**Check Python path:**
```bash
/Users/andrejs/easypost-mcp-project/backend/venv/bin/python --version
# Should show: Python 3.12.12
```

**Test MCP server manually:**
```bash
cd /Users/andrejs/easypost-mcp-project/backend
source venv/bin/activate
python run_mcp.py
```

Press Ctrl+C to exit. If it starts without errors, the server is configured correctly.

### API Key Issues

If you see authentication errors, verify your API key:

```bash
cd /Users/andrejs/easypost-mcp-project/backend
source venv/bin/activate
python -c "from src.utils.config import settings; settings.validate(); print('✓ API key valid')"
```

### View Claude Desktop Logs

**macOS logs location:**
```bash
~/Library/Logs/Claude/mcp*.log
```

**View recent errors:**
```bash
tail -f ~/Library/Logs/Claude/mcp-server-easypost-shipping.log
```

### Environment Variables Not Loading

If the server can't find modules:

1. Check `PYTHONPATH` in config matches your project path
2. Ensure absolute paths are used (no `~` or relative paths)
3. Verify `.env` file exists in backend directory

## Alternative: Using HTTP Transport

If stdio mode has issues, you can run the HTTP server separately:

### Start HTTP Server

```bash
cd /Users/andrejs/easypost-mcp-project/backend
./start_backend.sh
```

Server runs at `http://localhost:8000`

### Claude Desktop Config (HTTP Mode)

```json
"easypost-shipping-http": {
  "url": "http://localhost:8000/mcp"
}
```

**Note**: You must manually start the HTTP server before using Claude Desktop with this method.

## Security Notes

⚠️ **API Key in Config**: The API key is stored in plain text in the Claude Desktop config. This is acceptable for:
- Test/development API keys
- Local development environments
- Single-user machines

For production:
- Use environment variables loaded from secure storage
- Rotate API keys regularly
- Use read-only API keys if available

## Quick Reference

**Config File**: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Backup Config**:
```bash
cp ~/Library/Application\ Support/Claude/claude_desktop_config.json{,.backup}
```

**Restore Backup**:
```bash
cp ~/Library/Application\ Support/Claude/claude_desktop_config.json{.backup,}
```

**Restart Claude**: Cmd+Q then reopen

**Test Server**: 
```bash
cd backend && source venv/bin/activate && python run_mcp.py
```

## Need Help?

1. Check logs: `~/Library/Logs/Claude/mcp*.log`
2. Verify Python version: Should be 3.12+
3. Test server manually before configuring Claude
4. Ensure all paths in config are absolute (no `~`)
