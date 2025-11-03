Process bulk shipments with EasyPost MCP (M3 Max optimized - 16 workers).

**Domain**: EasyPost shipping and logistics  
**MCP Tool**: easypost-shipping server  
**Performance**: 5 shipments/second (150 in 30s)

## Usage

```bash
# Paste spreadsheet data directly
/bulk-ship [spreadsheet data]

# With specific origin city
/bulk-ship --from=Las Vegas [data]

# Preview without processing
/bulk-ship --dry-run [data]
```

## What It Does

**Intelligent Bulk Processing:**
1. Parses tab-separated spreadsheet data
2. Auto-detects origin state and city
3. Validates addresses and parcel data
4. Gets rates from multiple carriers (parallel)
5. Provides recommendations (cheapest, fastest)
6. Reports processing statistics

## MCP Integration

**Server**: easypost-shipping  
**Tool**: `parse_and_get_bulk_rates`

**Execution Chain:**
1. **Parse** spreadsheet data (validates 16 columns)
2. **Detect** origin from first row (California/Nevada)
3. **Parallel Processing** (16 workers on M3 Max):
   - Each worker processes batch of shipments
   - Gets rates from EasyPost API
   - Handles errors gracefully
4. **Aggregate** results and calculate summary
5. **Report** with recommendations

**Progress Reporting:**
- Real-time: "Processing shipment 45/150..."
- Shows: Success count, failure count
- Displays: Estimated time remaining

## Expected Input Format

**Tab-separated with 16 columns:**
```
Origin_State	Carrier	First_Name	Last_Name	Phone	Email	Street1	Street2	City	State	ZIP	Country	Type	Dimensions	Weight	Contents
California	USPS	John	Doe	555-0100	john@example.com	123 Main St		Los Angeles	CA	90001	US	Package	12 x 9 x 6	1.5 lbs	Beauty products
Nevada	FedEx	Jane	Smith	555-0101	jane@example.com	456 Oak Ave	Apt 2	Las Vegas	NV	89101	US	Package	10 x 8 x 4	2.3 lbs	Wellness items
```

## Auto-Detection

**Origin Detection:**
- Reads `Origin_State` from first row
- Maps to default city:
  - California → Los Angeles
  - Nevada → Las Vegas
- Override with `--from=<city>`

**Store Addresses:**
- Pre-configured for CA (LA, SF, SD)
- Pre-configured for NV (Las Vegas, Reno)
- Uses realistic retail addresses

## Output Format

```
📦 Bulk Shipment Processing (M3 Max: 16 workers)

📊 Analysis:
- Total shipments: 150
- Origin: Los Angeles, CA (auto-detected)
- Processing with 16 parallel workers

🚀 Processing (real-time updates)...
[█████████████████-----] 85/150 (56%)
Estimated time: 28s remaining

✅ Results:

Successful: 145/150 (96.7%)
Failed: 5/150 (3.3%)

Performance:
- Total time: 29.4s
- Throughput: 5.1 shipments/second
- Workers: 16
- Speedup: 10.2x vs sequential

Top Rates:
1. USPS Priority: $8.50 avg (fastest for <2lbs)
2. FedEx Ground: $12.30 avg (best for >5lbs)
3. UPS Ground: $11.80 avg (reliable)

Failed Shipments:
- Line 23: Invalid ZIP code
- Line 67: Parcel too large
- Line 89: Missing street address
- Line 102: Invalid state code
- Line 134: Weight exceeds limit

💾 Results saved to: bulk_shipments_20251103_143022.json
```

## Performance (M3 Max)

**Parallel Processing:**
- Workers: 16 simultaneous API calls
- Batch size: 150 optimal for M3 Max
- Throughput: 5 shipments/second
- Memory: Efficient (4GB per worker)

**Expected Times:**
- 10 shipments: 2-3s
- 50 shipments: 10-12s
- 100 shipments: 18-22s
- 150 shipments: 28-32s
- 500 shipments: 90-110s

## Error Handling

**Graceful Degradation:**
- Invalid data: Skips and reports
- API errors: Retries with backoff
- Rate limits: Queues requests
- Network issues: Marks for retry

**All errors reported** in final output with line numbers.

## Advanced Options

```bash
# Specify origin city
/bulk-ship --from="San Francisco" [data]

# Only get rates (don't create shipments)
/bulk-ship --rates-only [data]

# Specific carrier preference
/bulk-ship --carrier=USPS [data]

# Export format
/bulk-ship --export=csv [data]
/bulk-ship --export=json [data]
```

## Integration with EasyPost MCP

**Direct MCP tool call:**
```python
# Backend: backend/src/mcp/tools/bulk_tools.py
@mcp.tool()
async def parse_and_get_bulk_rates(
    spreadsheet_data: str,
    from_city: str = None,
    ctx: Context = None
) -> dict:
    # 16 parallel workers
    # Progress reporting via ctx
    # Returns rates for all shipments
```

**This command is a user-friendly wrapper!**

## Use Cases

**1. Daily Fulfillment:**
- Export orders from e-commerce
- Paste into /bulk-ship
- Get instant rate comparisons
- Choose best carrier per shipment

**2. Rate Shopping:**
- Test different scenarios
- Compare carrier costs
- Optimize shipping strategy

**3. Address Validation:**
- Verify bulk addresses
- Catch errors before shipping
- Save on failed deliveries

## Related Commands

```bash
/test backend/tests/integration/test_bulk*.py  # Test bulk processing
/explain backend/src/mcp/tools/bulk_tools.py   # Understand code
/fix                                            # Fix bulk processing errors
```

**EasyPost-specific bulk processing - optimized for M3 Max!**
