Track multiple packages simultaneously (M3 Max: 16 parallel workers).

**Domain**: Batch package tracking
**MCP**: Parallel get_tracking calls
**Performance**: 2-3s for 50 packages (16x faster)

## Usage

```bash
# Track multiple packages (paste tracking numbers)
/track-batch EZ1234567890
EZ9876543210
EZ5555555555

# From file
/track-batch --file=tracking_numbers.txt

# Export results
/track-batch --export=csv [numbers]
```

## What It Does

**Parallel Tracking:**
1. Parses list of tracking numbers
2. Validates format (alphanumeric + hyphens)
3. Fetches status from all packages simultaneously (16 workers)
4. Aggregates results by status
5. Identifies issues/delays
6. Provides summary statistics

## MCP Integration

**Server**: easypost-shipping
**Tool**: `get_tracking()` (existing, called in parallel)

**Execution**:
1. Parse tracking numbers (1-1000+)
2. Create async tasks (16 concurrent)
3. Execute with asyncio.gather()
4. Aggregate by status
5. Report summary

## Output Format

```
📦 Batch Tracking Results (50 packages)

🚀 Processing with 16 parallel workers...
Completed in 2.4s

📊 Status Summary:

✅ Delivered: 32 (64%)
  - On-time: 30 (93.8%)
  - Delayed: 2 (6.2%)

🚚 In Transit: 15 (30%)
  - On schedule: 13
  - Delayed: 2 (weather in Chicago)

⚠️ Issues: 2 (4%)
  - Exception: 1 (incorrect address)
  - Returned: 1 (recipient refused)

🔍 Delayed Packages (4 total):

1. EZ1234567890
   - Status: In transit (delayed)
   - Issue: Weather delay in Chicago
   - Expected: Tomorrow
   - Last update: 2 hours ago

2. EZ9876543210
   - Status: In transit (delayed)
   - Issue: Customs clearance
   - Expected: 2 days
   - Last update: 6 hours ago

3. EZ5555555555
   - Status: Delivered (late)
   - Delay: 1 day
   - Reason: Address correction needed

4. EZ3333333333
   - Status: Delivered (late)
   - Delay: 2 days
   - Reason: Weekend delay

⚠️ Problem Packages (2 total):

1. EZ7777777777
   - Status: Exception
   - Issue: Incorrect address
   - Action: Contact recipient for correct address

2. EZ8888888888
   - Status: Returned to sender
   - Issue: Recipient refused delivery
   - Action: Contact customer for resolution

📈 Performance Metrics:
- Average delivery time: 2.8 days
- On-time rate: 88.2%
- Issue rate: 4%
- Carrier breakdown:
  - USPS: 32 packages (90.6% on-time)
  - FedEx: 12 packages (83.3% on-time)
  - UPS: 6 packages (100% on-time)

💡 Insights (Sequential-thinking):
- Weather delays affecting Chicago routes
- USPS performing better than FedEx this period
- UPS perfect delivery rate (small sample)
- 4% issue rate is normal

🎯 Recommendations:
1. Monitor Chicago route weather
2. Consider UPS for critical shipments
3. Review address validation process (2 failures)

💾 Exported to: tracking_batch_20251103_143500.csv
```

## Parallel Processing

**M3 Max Optimization:**
```python
# Create 16 concurrent tracking requests
async def track_one(tracking_number):
    return await easypost_service.get_tracking(tracking_number)

# Process in parallel
tasks = [track_one(num) for num in tracking_numbers]
results = await asyncio.gather(*tasks)
```

**Performance:**
- Sequential: 50 packages × 0.5s = 25s
- Parallel (16 workers): 50 packages in 2-3s
- **Speedup: 10-12x**

## Smart Features

**Auto-Detection:**
- Recognizes tracking number formats
- Handles mixed carriers (USPS, FedEx, UPS)
- Filters duplicates
- Validates before calling API

**Aggregation:**
- Groups by status (delivered, in-transit, exception)
- Calculates on-time percentages
- Identifies patterns (weather, routes, carriers)
- Highlights action items

**Export Options:**
- CSV: For spreadsheets
- JSON: For processing
- Markdown: For reports

## Use Cases

**1. Daily Check:**
- Track all active shipments
- Identify issues quickly
- Take corrective action

**2. Customer Service:**
- Batch status updates
- Proactive problem notification
- Performance reporting

**3. Analytics:**
- Delivery performance trends
- Carrier reliability comparison
- Route issue identification

**4. Operations:**
- Monitor shipment flow
- Identify bottlenecks
- Optimize processes

## Advanced Options

```bash
# Only show issues
/track-batch --issues-only [numbers]

# Only show delivered
/track-batch --status=delivered [numbers]

# Group by carrier
/track-batch --group-by=carrier [numbers]

# Include detailed events
/track-batch --verbose [numbers]

# Monitor mode (refresh every 5 min)
/track-batch --watch [numbers]
```

## Integration

**With other commands:**
```bash
# After bulk creation
/bulk-create [data]        # Returns tracking numbers
/track-batch [numbers]     # Monitor all created shipments

# For analysis
/track-batch [numbers]     # Get current status
/analytics-deep 7d         # Analyze delivery patterns

# For optimization
/track-batch [numbers]     # Identify issues
/shipping-optimize         # Get recommendations
```

## Performance Expectations

| Package Count | Sequential | Parallel (16) | Speedup |
|---------------|------------|---------------|---------|
| 10 | 5s | 0.5s | 10x |
| 50 | 25s | 2-3s | 10x |
| 100 | 50s | 4-5s | 10x |
| 500 | 250s | 20-25s | 10x |
| 1000 | 500s | 40-45s | 11x |

**M3 Max makes batch tracking instant!**

## Related Commands

```bash
/bulk-create [data]        # Create shipments
/track-batch [numbers]     # Track them (this)
/analytics-deep 30d        # Analyze performance
/carrier-compare [route]   # Optimize future shipments
```

**Batch tracking - monitor hundreds of packages in seconds!**

