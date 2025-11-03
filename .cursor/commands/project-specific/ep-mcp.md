Test and interact with EasyPost MCP tools directly.

**Domain**: MCP tool development
**Performance**: Direct tool invocation

## Usage

```bash
# List all MCP tools
/ep-mcp list

# Test specific tool
/ep-mcp test create_shipment
/ep-mcp test get_rates
/ep-mcp test parse_and_get_bulk_rates

# Interactive tool tester
/ep-mcp interactive

# Validate tool schemas
/ep-mcp validate
```

## What It Does

**MCP Tool Testing:**
1. Lists all registered MCP tools
2. Shows tool schemas and parameters
3. Provides interactive testing interface
4. Validates input/output schemas
5. Tests error handling

## MCP Integration

**Server**: Desktop Commander + EasyPost MCP
**Direct Tool Invocation**

**List Tools:**
```python
from src.mcp import mcp

# Get all registered tools
tools = mcp.list_tools()
for tool in tools:
    print(f"{tool.name}: {tool.description}")
```

**Test Tool:**
```python
# Invoke tool with test data
result = await mcp.call_tool(
    "create_shipment",
    {
        "to_address": {...},
        "from_address": {...},
        "parcel": {...}
    }
)
```

## Output Format

### List All Tools

```
╔═══════════════════════════════════════════════════════════╗
║         EASYPOST MCP TOOLS (15 registered)               ║
╚═══════════════════════════════════════════════════════════╝

📦 SHIPMENT TOOLS (3)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  create_shipment
    Create and purchase a shipping label
    Parameters: to_address, from_address, parcel, carrier

  buy_shipment
    Purchase label for existing shipment
    Parameters: shipment_id, rate_id

  list_shipments
    Get list of shipments
    Parameters: page_size, purchased, start_datetime, end_datetime

🔍 TRACKING TOOLS (1)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  get_tracking
    Get tracking information
    Parameters: tracking_number

💰 RATE TOOLS (1)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  get_rates
    Get available shipping rates
    Parameters: to_address, from_address, parcel

📊 BULK TOOLS (2)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  parse_and_get_bulk_rates
    Get rates for multiple shipments
    Parameters: spreadsheet_data, from_city, ctx

  create_bulk_shipments
    Create multiple shipments in parallel (16 workers)
    Parameters: spreadsheet_data, from_city, purchase_labels,
                carrier, dry_run, ctx

📁 RESOURCES (3)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  shipment_template
  bulk_rates_template
  carrier_guide

💬 PROMPTS (2)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  create_shipment_guide
  troubleshoot_shipment
```

### Test Specific Tool

```
╔═══════════════════════════════════════════════════════════╗
║       TESTING: create_bulk_shipments                      ║
╚═══════════════════════════════════════════════════════════╝

Tool Schema:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Parameters:
  - spreadsheet_data (string, required): Tab-separated data
  - from_city (string, optional): Origin city
  - purchase_labels (boolean, optional): Buy labels (default: true)
  - carrier (string, optional): Force specific carrier
  - dry_run (boolean, optional): Validate only (default: false)
  - ctx (Context, optional): MCP context for progress

Running test...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Input:
{
  "spreadsheet_data": "California\tUSPS\tJohn\tDoe...",
  "from_city": "Los Angeles",
  "dry_run": true
}

Output:
{
  "status": "success",
  "data": {
    "dry_run": true,
    "validation": {
      "total": 3,
      "valid": 3,
      "invalid": 0
    }
  },
  "message": "Dry-run: 3/3 valid",
  "timestamp": "2025-11-03T17:35:00Z"
}

Duration: 0.15s
Result: ✅ PASS

Schema Validation:
  Input: ✅ Valid
  Output: ✅ Valid

Error Handling:
  Missing required params: ✅ Raises error
  Invalid data type: ✅ Raises error
  API error: ✅ Handled gracefully
```

### Interactive Mode

```
╔═══════════════════════════════════════════════════════════╗
║       MCP INTERACTIVE TOOL TESTER                         ║
╚═══════════════════════════════════════════════════════════╝

Available tools: 15

Enter tool name (or 'list' to see all, 'exit' to quit):
> create_shipment

Tool: create_shipment
Description: Create and purchase a shipping label

Enter parameters (JSON format):
{
  "to_address": {
    "name": "John Doe",
    "street1": "123 Main St",
    "city": "New York",
    "state": "NY",
    "zip": "10001",
    "country": "US"
  },
  "from_address": {
    "name": "Test Sender",
    "street1": "456 Oak Ave",
    "city": "Los Angeles",
    "state": "CA",
    "zip": "90001",
    "country": "US"
  },
  "parcel": {
    "length": 12,
    "width": 9,
    "height": 6,
    "weight": 32
  }
}

Calling tool...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Result:
{
  "status": "success",
  "id": "shp_abc123",
  "tracking_code": "9400110200881234567890",
  "rates": [...],
  "postage_label_url": "https://..."
}

Duration: 1.2s
Status: ✅ SUCCESS

Test another tool? (y/n):
```

### Validate Schemas

```
╔═══════════════════════════════════════════════════════════╗
║       MCP SCHEMA VALIDATION                               ║
╚═══════════════════════════════════════════════════════════╝

Validating all tool schemas...

create_shipment:
  ✅ Parameters schema valid
  ✅ Return type annotated
  ✅ Docstring complete
  ✅ Error handling present

get_tracking:
  ✅ Parameters schema valid
  ✅ Return type annotated
  ✅ Docstring complete
  ✅ Error handling present

parse_and_get_bulk_rates:
  ✅ Parameters schema valid
  ✅ Return type annotated
  ✅ Docstring complete
  ⚠️ Warning: Large input validation missing

create_bulk_shipments:
  ✅ Parameters schema valid
  ✅ Return type annotated
  ✅ Docstring complete
  ✅ Error handling present
  ✅ Progress reporting implemented

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ VALIDATION SUMMARY

Total tools: 15
Passed: 14
Warnings: 1
Failed: 0

Recommendation: Add input size validation to bulk_rates
```

## Testing Workflows

### Bulk Creation Workflow
```bash
# Test with sample data
/ep-mcp test create_bulk_shipments

# Dry-run validation
/ep-mcp test create_bulk_shipments --dry-run

# Full workflow with labels
/ep-mcp test create_bulk_shipments --purchase-labels
```

### Error Handling Tests
```bash
# Test with invalid data
/ep-mcp test create_shipment --invalid-address

# Test with missing API key
/ep-mcp test get_rates --no-auth

# Test with rate limits
/ep-mcp test create_bulk_shipments --stress
```

## Related Commands

```bash
/ep-mcp list           # List tools (this)
/ep-mcp test [tool]    # Test specific tool
/ep-dev                # Start dev environment
/ep-test               # Run all tests
```

**Direct MCP tool testing - no MCP client needed!**

