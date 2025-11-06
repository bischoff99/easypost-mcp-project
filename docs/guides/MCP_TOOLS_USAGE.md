# Using MCP Tools in Cursor IDE

**Last Updated**: 2025-11-06
**Configuration**: Fixed and verified ✅

---

## Quick Start

### 1. Restart Cursor IDE

**Required**: Cmd+Q → Reopen Cursor

MCP configuration changes only take effect after restart.

---

### 2. Verify MCP Server Running

After restart, check Cursor status bar or settings for "easypost" MCP server.

**If not showing**:
- Check `~/.cursor/mcp.json` configuration
- Verify `EASYPOST_API_KEY` is set in environment
- Check logs in Cursor output panel

---

### 3. Use MCP Tools

**No special syntax needed** - just ask naturally!

Cursor will automatically detect and use the appropriate MCP tool.

---

## Available MCP Tools (6)

### 1. create_shipment

**Purpose**: Create single shipment with label purchase

**Example**:
```
Create a USPS shipment from San Francisco, CA to
David Thomas, 79 Upper Malvern Road, Belfast BT86XN UK
for a baseball glove (12x12x4 inches, 3.2 lbs, $44)
```

**What happens**:
- Validates addresses
- Creates customs info (international)
- Gets rates from carrier
- Purchases label
- Returns tracking number

---

### 2. track_shipment

**Purpose**: Track package by tracking number

**Example**:
```
Track shipment 9400111899223835948292
```

**Returns**:
- Current status
- Location
- Estimated delivery
- Tracking history

---

### 3. get_rates

**Purpose**: Compare carrier rates without purchasing

**Example**:
```
Get shipping rates from Los Angeles to London
for a 10x10x10 inch, 5 lb package
```

**Returns**:
- Rates from all carriers
- Delivery times
- Price comparison

---

### 4. parse_and_get_bulk_rates

**Purpose**: Get rates for multiple shipments from spreadsheet

**Example**:
```
Parse this spreadsheet data and get rates:

California	USPS	DAVID	THOMAS	+447852711321	...
Nevada	FedEx	JOHN	SMITH	+442071234567	...
```

**Returns**:
- Rates for all shipments
- Warehouse assignments
- Cost breakdown

---

### 5. create_bulk_shipments

**Purpose**: Create multiple shipments in parallel (M3 Max optimized)

**Example**:
```
Create bulk shipments with dry-run first:
<paste spreadsheet data>

Use dry_run=True to validate without charges
```

**Features**:
- 16 parallel workers (M3 Max)
- Dry-run mode
- Two-phase workflow (get rates → approve → buy)
- Progress reporting

---

### 6. buy_bulk_shipments

**Purpose**: Purchase labels for pre-created shipments

**Example**:
```
Buy labels for these shipment IDs:
shp_123, shp_456, shp_789

Use carrier: USPS
```

**Use Case**: Two-phase workflow
1. Create bulk shipments (no purchase)
2. Review rates
3. Approve specific shipments
4. Buy only approved labels

---

## Configuration Details

### MCP Server Config (`~/.cursor/mcp.json`)

```json
{
  "mcpServers": {
    "easypost": {
      "command": "/Users/andrejs/Developer/github/andrejs/easypost-mcp-project/backend/venv/bin/python",
      "args": ["run_mcp.py"],
      "cwd": "/Users/andrejs/Developer/github/andrejs/easypost-mcp-project/backend",
      "env": {
        "EASYPOST_API_KEY": "${EASYPOST_API_KEY}",
        "DATABASE_URL": "postgresql://easypost:easypost@localhost:5432/easypost_mcp",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

---

### Environment Variables Required

**EASYPOST_API_KEY**: Get from Keychain or `.env`
```bash
security find-generic-password -s easypost-prod -w
```

**DATABASE_URL**: PostgreSQL connection
```
postgresql://easypost:easypost@localhost:5432/easypost_mcp
```

---

## Troubleshooting

### MCP Server Not Starting

**Check**:
1. Python venv exists: `backend/venv/bin/python`
2. Dependencies installed: `pip list | grep fastmcp`
3. run_mcp.py exists: `ls backend/run_mcp.py`
4. Environment vars set: `echo $EASYPOST_API_KEY`

**Fix**:
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

---

### MCP Tools Not Showing

**Check**:
1. Cursor restarted after config change
2. ~/.cursor/mcp.json has correct path
3. Check Cursor output panel for errors

---

### Tool Execution Fails

**Check**:
1. Database running: `psql -d easypost_mcp -c "SELECT 1"`
2. EasyPost API key valid
3. Check backend logs

---

## Examples

### International Shipment (Your Data)

```
Create a USPS shipment:

From: California Warehouse, San Francisco, CA
To: David Thomas
    79 Upper Malvern Road
    Four Winds
    Belfast BT86XN
    Northern Ireland, UK
    +447852711321
    irishdave68@protonmail.com

Package: 12x12x4 inches, 3.2 lbs
Contents: Pro-Series Infield Baseball Glove - 12" Training Model
Value: $44
HTS Code: 9506.99.6080
```

MCP tool will:
1. Validate addresses
2. Create customs declaration
3. Get USPS rates
4. Purchase label
5. Return tracking number

---

### Bulk Processing

```
Parse and get rates for this spreadsheet:

California	USPS	DAVID	THOMAS	+447852711321	irishdave68@protonmail.com	79	UPPER MALVERN ROAD	FOUR WINDS	BELFAST 	BT86XN	NORTHERN IRELAND UNITED KINGDOM 	FALSE	12 x 12 x 4	3.2 lbs	(1) Pro-Series Infield Baseball Glove – 12" Training Model HTS Code: 9506.99.6080 ($44)
Nevada	FedEx	JOHN	SMITH	+442071234567	john@example.com	10	High Street		London	W1A 1AA	ENGLAND UNITED KINGDOM	FALSE	10 x 10 x 10	5 lbs	(2) Widget ($25 each)
```

MCP tool will:
1. Parse all rows
2. Detect warehouses
3. Create customs for international
4. Get rates from all carriers
5. Return comparison table

---

## MCP Resources

Beyond tools, you also have **MCP resources**:

### shipment://list
```
Show me recent shipments
```

### stats://summary
```
What are my shipping analytics?
```

---

## MCP Prompts

AI-assisted workflows:

- Shipping optimization
- Carrier comparison
- Cost analysis
- Route planning

Just ask naturally - prompts are auto-applied!

---

## Technical Details

### MCP Server Entry Point

**File**: `backend/run_mcp.py`

```python
from src.mcp import mcp

if __name__ == "__main__":
    mcp.run()  # Starts STDIO mode
```

---

### MCP Tools Location

**Directory**: `backend/src/mcp/tools/`

```
shipment_tools.py        # create_shipment
tracking_tools.py        # track_shipment
rate_tools.py            # get_rates
bulk_tools.py            # parse_and_get_bulk_rates
bulk_creation_tools.py   # create/buy bulk shipments
```

---

### Shared Business Logic

MCP tools use the same code as FastAPI:

```python
src/services/easypost_service.py    # EasyPost API wrapper
src/services/database_service.py    # PostgreSQL CRUD
src/models.py                       # SQLAlchemy models
```

**Result**: Same functionality, different protocol (STDIO vs HTTP)

---

## Next Steps

1. **Restart Cursor** (Cmd+Q → Reopen)
2. **Verify** MCP server in status bar
3. **Try it**: Ask me to create the Belfast shipment using MCP tools!

---

**Configuration complete - restart Cursor to activate MCP tools!**
