# MCP Tools & Resources Inventory

**Server**: EasyPost MCP Server
**Location**: `backend/src/mcp_server.py`
**Framework**: FastMCP 2.x

---

## 🔧 Tools (4)

### 1. `get_tracking`
**Purpose**: Get real-time tracking information for a shipment

**Parameters**:
- `tracking_number` (str) - The tracking number to look up

**Returns**:
```json
{
  "status": "success",
  "data": {
    "tracking_number": "EZ1234567890",
    "status": "in_transit",
    "carrier": "USPS",
    "est_delivery": "2025-11-05",
    "tracking_history": [...]
  },
  "message": "Tracking information retrieved",
  "timestamp": "2025-11-03T..."
}
```

---

### 2. `get_shipment_rates`
**Purpose**: Get shipping rates for single or multiple shipments

**Parameters**:
- `spreadsheet_data` (str) - Tab-separated shipment data (1+ lines)
- `ctx` (Context, optional) - MCP context for progress reporting

**Returns**: Rates for all shipments with comparison table

---

### 3. `create_shipment`
**Purpose**: Create single or multiple shipments in parallel (M3 Max optimized, 16 workers)

**Parameters**:
- `spreadsheet_data` (str) - Tab-separated shipment data
- `purchase_labels` (bool) - Whether to purchase labels immediately (default: False)
- `carrier` (str, optional) - Force specific carrier
- `dry_run` (bool) - Validate without creating (default: False)

**Returns**: Created shipments with rates and shipment IDs

---

### 4. `buy_shipment_label`
**Purpose**: Purchase labels for pre-created shipments using selected rates

**Parameters**:
- `shipment_ids` (list[str]) - List of shipment IDs
- `rate_ids` (list[str]) - List of rate IDs to use
- `customs_data` (list[dict], optional) - Customs information

**Returns**: Purchased labels with tracking numbers

---

### 5. `create_shipment` (Legacy - use bulk tools for single shipments)
**Purpose**: Create a new shipment and purchase a shipping label

**Parameters**:
- `to_address` (dict) - Destination address
  - name, street1, city, state, zip, country (optional)
- `from_address` (dict) - Origin address
  - name, street1, city, state, zip, country (optional)
- `parcel` (dict) - Package dimensions
  - length, width, height (inches), weight (ounces)
- `carrier` (str, optional) - Preferred carrier (default: "USPS")

**Returns**:
```json
{
  "status": "success",
  "data": {
    "shipment_id": "shp_xxx",
    "tracking_number": "EZ1234567890",
    "label_url": "https://...",
    "rate": "12.50",
    "carrier": "USPS"
  },
  "message": "Shipment created successfully",
  "timestamp": "2025-11-03T..."
}
```

**Example**:
```python
result = await create_shipment(
    to_address={"name": "John Doe", "street1": "123 Main St", ...},
    from_address={"name": "Jane Smith", "street1": "456 Market St", ...},
    parcel={"length": 10, "width": 8, "height": 6, "weight": 16},
    carrier="USPS"
)
```

---
**Purpose**: Get shipping rates from multiple carriers

**Parameters**:
- `to_address` (dict) - Destination address
- `from_address` (dict) - Origin address
- `parcel` (dict) - Package dimensions

**Returns**:
```json
{
  "status": "success",
  "data": [
    {
      "carrier": "USPS",
      "service": "Priority Mail",
      "rate": "12.50",
      "delivery_days": 2
    },
    ...
  ],
  "message": "Rates retrieved successfully",
  "timestamp": "2025-11-03T..."
}
```

**Example**:
```python
result = await get_rates(
    to_address={...},
    from_address={...},
    parcel={...}
)
```

---

## 📦 Resources (2)

### 1. `easypost://shipments/recent`
**Purpose**: Get list of recent shipments from EasyPost API

**Returns**: JSON list of recent shipments with:
- Shipment ID
- Tracking number
- Status
- Creation date
- Addresses (from/to)
- Label URL

**Usage**:
```python
# Accessed as MCP resource
shipments = mcp.read_resource("easypost://shipments/recent")
```

---

### 2. `easypost://stats/overview`
**Purpose**: Get shipping statistics overview

**Returns**: JSON with:
- Total shipments count
- Active deliveries
- Total cost
- Average cost per shipment
- Success rate

**Usage**:
```python
stats = mcp.read_resource("easypost://stats/overview")
```

---

## 💡 Prompts (5)

### 1. `compare_carriers`
**Purpose**: Compare shipping rates across carriers

**Parameters**:
- origin (str) - Origin city/state
- destination (str) - Destination city/state
- weight_oz (float) - Package weight in ounces
- length, width, height (float) - Dimensions in inches

**Workflow**:
1. Fetch rates from all carriers
2. Compare prices and delivery times
3. Create comparison table
4. Recommend best option (lowest cost, fastest, best value)

---

### 2. `track_and_notify`
**Purpose**: Track a shipment and set up notifications

**Parameters**:
- tracking_number (str) - Tracking number
- notification_email (str) - Email for updates

**Workflow**:
1. Retrieve current tracking status
2. Parse tracking events
3. Estimate delivery date
4. Set up notification preferences
5. Create timeline visualization

---

### 3. `cost_optimization`
**Purpose**: Analyze shipping costs and suggest optimizations

**Parameters**:
- time_period (str) - Analysis period (e.g., "last_30_days")

**Workflow**:
1. Retrieve shipment history
2. Analyze cost patterns
3. Identify optimization opportunities
4. Calculate potential savings
5. Provide actionable recommendations

---

### 4. `bulk_rate_check`
**Purpose**: Check rates for multiple shipments at once

**Parameters**:
- shipments_list (list) - List of shipment details

**Workflow**:
1. Process each shipment
2. Get rates for all
3. Create cost comparison table
4. Identify best carriers per shipment
5. Calculate total savings

---

## 🎯 Tool Usage Summary

| Type | Count | Purpose |
|------|-------|---------|
| **Tools** | 4 | Core shipping operations (tracking, rates, bulk create, bulk purchase) |
| **Resources** | 2 | Data access (shipments, stats) |
| **Prompts** | 5 | Guided workflows |
| **Total** | **11** | Complete MCP integration |

---

## 🔌 Integration Points

### FastMCP Server
- **Entry Point**: `backend/src/mcp_server.py`
- **Runner**: `backend/run_mcp.py` (stdio mode)
- **HTTP Mode**: Integrated in `backend/src/server.py`

### REST API Equivalent
All MCP tools have REST API endpoints:
- `create_shipment` → `POST /api/shipments`
- `get_tracking` → `GET /api/tracking/{number}`
- `get_rates` → `POST /api/rates`

### Configuration
```json
{
  "mcpServers": {
    "easypost-shipping": {
      "command": "python",
      "args": ["/path/to/run_mcp.py"],
      "env": {
        "EASYPOST_API_KEY": "your_key_here"
      }
    }
  }
}
```

---

## 📝 Example Usage

### Create Shipment with MCP
```python
import mcp

result = await mcp.call_tool(
    "create_shipment",
    to_address={
        "name": "John Doe",
        "street1": "123 Main St",
        "city": "New York",
        "state": "NY",
        "zip": "10001"
    },
    from_address={...},
    parcel={"length": 10, "width": 8, "height": 6, "weight": 16}
)
```

### Use Prompt for Comparison
```python
comparison = await mcp.use_prompt(
    "compare_carriers",
    origin="San Francisco, CA",
    destination="New York, NY",
    weight_oz=16,
    length=10,
    width=8,
    height=6
)
```

---

## ✅ Tool Validation

All tools:
- ✅ Properly decorated with @mcp.tool()
- ✅ Complete docstrings
- ✅ Type hints provided
- ✅ Error handling implemented
- ✅ Standardized response format
- ✅ Context logging support

---

**Status**: All 11 MCP tools/resources/prompts are production-ready and fully documented!

**Note**: Shipment tools (`get_shipment_rates`, `create_shipment`, `buy_shipment_label`) handle both single and multiple shipments, making separate single-shipment tools unnecessary.
