Deep analytics with parallel processing and AI insights (M3 Max: 16 workers).

**Domain**: Shipping business intelligence
**MCP Chain**: Parallel stats → Sequential-thinking insights
**Performance**: 5-10s for 1000 shipments (10x faster)

## Usage

```bash
# Last 7 days
/analytics-deep 7d

# Last 30 days
/analytics-deep 30d

# Custom date range
/analytics-deep --from=2025-10-01 --to=2025-11-03

# Specific focus
/analytics-deep 30d --focus=cost
/analytics-deep 30d --focus=carriers
/analytics-deep 30d --focus=routes
```

## What It Does

**Parallel Analytics Processing:**
1. Fetches shipment data (from API or database)
2. Processes metrics in parallel (16 workers):
   - Cost analysis per carrier
   - Volume trends by date
   - Route performance
   - Delivery success rates
3. Sequential-thinking identifies:
   - Patterns and trends
   - Cost-saving opportunities
   - Performance issues
   - Optimization recommendations

## MCP Integration

**Stage 1 - Data Fetch** (easypost-shipping):
- Tool: Get shipments for time period
- Parallel: Fetch in batches if large dataset
- Time: 2-3s

**Stage 2 - Parallel Processing** (M3 Max optimization):
- Method: asyncio.gather() with 16 workers
- Process: Calculate metrics concurrently
- Aggregation: Carrier stats, route stats, time series
- Time: 1-2s for 1000 shipments

**Stage 3 - AI Insights** (Sequential-thinking):
- Analyzes: Aggregated data (10-12 thoughts)
- Identifies: Trends, anomalies, opportunities
- Recommends: Actionable improvements
- Time: 5-7s

## Output Format

```
📊 Deep Analytics Report (Last 30 Days)

Performance Metrics:
- Total shipments: 1,247
- Total cost: $10,582.40
- Average cost: $8.48
- Delivery success rate: 94.2%

📈 Volume Trends:
Week 1: 284 shipments (↑12% vs avg)
Week 2: 298 shipments (↑16% vs avg)
Week 3: 312 shipments (↑21% vs avg)
Week 4: 353 shipments (↑37% vs avg)

Trend: Growing 8.2% week-over-week

🚚 Carrier Performance:

1. USPS (782 shipments, 62.7%)
   - Total cost: $6,625.60 ($8.47 avg)
   - On-time rate: 96.1%
   - Best for: <2 lbs, residential
   - Savings: $1,247 vs competitors

2. FedEx (327 shipments, 26.2%)
   - Total cost: $2,845.20 ($8.70 avg)
   - On-time rate: 93.8%
   - Best for: 2-10 lbs, commercial
   - Premium: $328 vs USPS for same routes

3. UPS (138 shipments, 11.1%)
   - Total cost: $1,111.60 ($8.05 avg)
   - On-time rate: 95.2%
   - Best for: >10 lbs, signature required
   - Value: Cheapest for heavy packages

🗺️ Top Routes:

1. LA → New York (245 shipments)
   - Cost: $2,082.50 ($8.50 avg)
   - Best carrier: USPS Priority (87% usage)

2. LA → Chicago (178 shipments)
   - Cost: $1,512.80 ($8.50 avg)
   - Best carrier: USPS Priority (92% usage)

3. Las Vegas → Miami (134 shipments)
   - Cost: $1,407.20 ($10.50 avg)
   - Best carrier: FedEx Ground (64% usage)

🧠 AI Insights (Sequential-thinking):

Observation 1: 62% USPS usage indicates lightweight inventory
Observation 2: Week-over-week growth is accelerating
Observation 3: FedEx premium ($328) may be unnecessary
Observation 4: LA → NY route dominates (20% of volume)

Pattern Identified: USPS Priority is overused
- 782 USPS shipments
- 23% could switch to First Class (save $784)
- Criteria: Non-urgent + <1 lb packages

Cost Optimization Opportunity:
💰 Potential savings: $784/month ($9,408/year)
Action: Route <1 lb non-urgent to USPS First Class

Speed Optimization Opportunity:
⚡ 47 shipments used Ground when 2Day available
Action: Auto-select 2Day for urgent tags

Carrier Mix Recommendation:
- USPS Priority: 55% (reduce from 63%)
- USPS First Class: 20% (increase from 0%)
- FedEx Ground: 18% (reduce from 26%)
- UPS Ground: 7% (reduce from 11%)

Expected impact: 7.4% cost reduction while maintaining speed

📈 Predictions (based on trends):
- Next week: ~385 shipments (9% growth)
- Next month: ~1,620 shipments
- Cost forecast: $13,730 (with current mix)
- Optimized forecast: $12,714 (with recommended mix)

🎯 Top 3 Recommendations:

1. Implement weight-based routing (<1 lb → First Class)
   - Impact: $784/month savings
   - Effort: Low (automation rule)
   - Timeline: Immediate

2. Optimize LA → NY route (20% of volume)
   - Current avg: $8.50
   - Opportunity: Negotiate bulk rate with USPS
   - Potential: 10-15% discount = $208/month

3. Review FedEx usage (26% of shipments)
   - 23% could use USPS (lighter packages)
   - Savings: $328/month
   - Action: Set carrier selection rules

💡 Summary:
Total potential savings: $1,320/month (12.5% cost reduction)
No service degradation
Automated implementation possible
```

## Parallel Processing Details

**M3 Max Optimization:**
```python
# Process metrics in parallel
async def calculate_carrier_metrics(shipments, carrier):
    # Process this carrier's shipments
    return metrics

# 16 parallel workers
tasks = [
    calculate_carrier_metrics(shipments, "USPS"),
    calculate_carrier_metrics(shipments, "FedEx"),
    calculate_carrier_metrics(shipments, "UPS"),
    # ... more calculations
]
results = await asyncio.gather(*tasks)
```

**Performance Gain:**
- Sequential: 10-15s for 1000 shipments
- Parallel (16 workers): 1-2s
- **10x faster!**

## Focus Areas

**Cost Focus** (`--focus=cost`):
- Detailed cost breakdown
- Savings opportunities
- Price trends
- Carrier cost comparison

**Speed Focus** (`--focus=speed`):
- Delivery time analysis
- On-time performance
- Route timing patterns
- Express vs ground usage

**Carrier Focus** (`--focus=carriers`):
- Carrier performance comparison
- Reliability metrics
- Service quality
- Usage patterns

**Route Focus** (`--focus=routes`):
- Top routes analysis
- Route-specific carrier performance
- Geographic patterns
- Zone-based optimization

## Related Commands

```bash
/analytics-deep 30d        # This command
/carrier-compare [route]   # Use insights for decisions
/shipping-optimize         # Get optimization plan
/bulk-create [data]        # Apply optimizations
```

**Deep business intelligence - AI-powered, M3 Max fast!**

