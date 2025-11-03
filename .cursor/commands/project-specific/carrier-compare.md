AI-powered carrier comparison and recommendations.

**Domain**: Shipping cost and speed optimization
**MCP Chain**: get_rates → Sequential-thinking analysis
**Performance**: 10-15s for comprehensive analysis

## Usage

```bash
# Compare carriers for a route
/carrier-compare "LA to NY" 12x9x6 2lbs

# With specific package details
/carrier-compare --from="Los Angeles, CA" --to="New York, NY" --dims=12x9x6 --weight=2lbs

# Focus on speed
/carrier-compare "LA to NY" 12x9x6 2lbs --priority=speed

# Focus on cost
/carrier-compare "LA to NY" 12x9x6 2lbs --priority=cost
```

## What It Does

**AI-Powered Carrier Analysis:**
1. Gets rates from all carriers (USPS, FedEx, UPS, DHL)
2. Sequential-thinking analyzes each option:
   - Cost analysis
   - Delivery time comparison
   - Reliability factors
   - Service features
3. Provides recommendation with reasoning
4. Suggests alternatives for different priorities

## MCP Integration

**Stage 1 - Get Rates** (easypost-shipping):
- Tool: `get_rates()`
- Returns: All available carrier rates
- Time: 3-5s

**Stage 2 - AI Analysis** (Sequential-thinking):
- Analyzes: Cost, speed, reliability
- Considers: Package characteristics, route
- Reasons: Step-by-step evaluation
- Recommends: Best carrier with explanation
- Time: 5-8s

**Stage 3 - Context Enhancement** (Context7, optional):
- Gets: Carrier performance data
- Historical: Reliability metrics
- Cache: 24h
- Time: 2-3s

## Output Format

```
🚚 Carrier Comparison Analysis

📦 Package Details:
- Route: Los Angeles, CA → New York, NY
- Dimensions: 12 x 9 x 6 inches
- Weight: 2 lbs (32 oz)
- Priority: Balanced (cost & speed)

📊 Available Rates (4 carriers):

1. USPS Priority Mail
   - Cost: $8.50
   - Delivery: 2-3 days
   - Features: Tracking, $100 insurance included
   - Reliability: 96% on-time

2. FedEx Ground
   - Cost: $12.30
   - Delivery: 3-5 days
   - Features: Tracking, signature confirmation
   - Reliability: 94% on-time

3. UPS Ground
   - Cost: $11.80
   - Delivery: 3-5 days
   - Features: Tracking, $100 insurance
   - Reliability: 95% on-time

4. USPS First Class
   - Cost: $5.20
   - Delivery: 3-5 days
   - Features: Tracking only
   - Reliability: 92% on-time

🧠 AI Analysis (Sequential-thinking):

Step 1: Package is lightweight (2 lbs) - favors USPS pricing
Step 2: Cross-country route - delivery time matters
Step 3: USPS Priority offers best speed/cost ratio
Step 4: FedEx/UPS premium not justified for this weight
Step 5: First Class too slow for 2-3 day target

Key insight: USPS Priority is the sweet spot for this shipment

💡 Recommendation: USPS Priority Mail

Why:
✅ Best cost ($8.50 vs $11-12 for competitors)
✅ Fastest delivery (2-3 days vs 3-5)
✅ Includes $100 insurance (no extra cost)
✅ Excellent reliability (96% on-time)
✅ Perfect for lightweight cross-country

Alternative scenarios:
- If urgent (<2 days): Use FedEx 2Day ($24.50)
- If budget <$6: Use USPS First Class (acceptable 3-5 days)
- If heavy (>10 lbs): FedEx/UPS become competitive

💰 Cost Comparison:
- Recommended: $8.50
- vs Cheapest: $5.20 (+$3.30 for 2 days faster)
- vs Most expensive: $12.30 (save $3.80)

⏱️ Time Comparison:
- Recommended: 2-3 days
- vs Fastest: Same (2-3 days)
- vs Slowest: 1-2 days faster

🎯 Confidence: 92%
Based on: Package weight, route distance, delivery window
```

## AI Reasoning Examples

**For Heavy Packages (10+ lbs):**
```
Step 1: Package weight (15 lbs) exceeds USPS Priority limit
Step 2: FedEx/UPS have better per-pound pricing
Step 3: Ground shipping adequate for non-urgent
Step 4: FedEx Ground slightly cheaper than UPS

Recommendation: FedEx Ground
Reasoning: Best per-pound rate for heavy packages
```

**For Urgent Delivery:**
```
Step 1: User priority is speed (--priority=speed)
Step 2: Filter for 1-2 day options only
Step 3: FedEx 2Day: $24.50, UPS 2nd Day: $26.20
Step 4: $1.70 difference negligible

Recommendation: FedEx 2Day
Reasoning: Faster + cheaper, proven reliability
```

## Performance

- Rate fetch: 3-5s
- AI analysis: 5-8s
- Context7 (optional): 2-3s (cached)
- **Total: 10-15s** for complete analysis

## Smart Defaults

**Auto-fills from context:**
- Origin: Uses last-used or defaults to LA
- Package type: Standard box
- Priority: Balanced (cost + speed)

**Learns from usage:**
- Remembers preferred carriers per route
- Suggests based on historical choices

## Advanced Features

```bash
# Multiple packages at once
/carrier-compare "LA to NY" 12x9x6 2lbs,10x8x5 3lbs,15x12x8 5lbs

# Compare across routes
/carrier-compare --routes="LA to NY,LA to Chicago,LA to Miami" 12x9x6 2lbs

# Historical analysis
/carrier-compare --analyze-history 30d

# What-if scenarios
/carrier-compare "LA to NY" 12x9x6 --weights=1,2,3,4,5lbs
```

## Integration with Other Commands

```bash
# Workflow 1: Rate shopping
/carrier-compare "LA to NY" 12x9x6 2lbs  # Get recommendation
/bulk-create --carrier=USPS [data]        # Use recommended carrier

# Workflow 2: Optimization
/analytics-deep 30d                       # Analyze patterns
/carrier-compare --optimize               # Get carrier mix recommendations

# Workflow 3: Cost analysis
/carrier-compare "LA to NY" 12x9x6 2lbs
/shipping-optimize                         # Overall cost optimization
```

## Use Cases

**1. Daily Rate Shopping:**
- Quick carrier decision
- AI removes guesswork
- Consistent optimization

**2. Route Planning:**
- Compare multiple routes
- Find best carrier per route
- Bulk optimization

**3. Cost Optimization:**
- Analyze spending patterns
- Find cheaper alternatives
- Reduce shipping costs

**4. Speed Optimization:**
- Urgent shipments
- Best express options
- Time-critical decisions

## Related Commands

```bash
/bulk-ship [data]          # Get bulk rates
/carrier-compare [route]   # AI recommendation (this)
/bulk-create [data]        # Create with recommended carrier
/analytics-deep            # Analyze carrier performance
```

**AI-powered shipping decisions - know the best carrier every time!**

