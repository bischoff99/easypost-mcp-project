AI-powered shipping optimization recommendations (Strategic analysis).

**Domain**: Shipping cost and performance optimization
**MCP**: Sequential-thinking strategy analysis
**Performance**: 15-20s for comprehensive recommendations

## Usage

```bash
# Full optimization analysis
/shipping-optimize

# Focus on cost reduction
/shipping-optimize --focus=cost

# Focus on speed
/shipping-optimize --focus=speed

# Focus on reliability
/shipping-optimize --focus=reliability

# Custom time period
/shipping-optimize --period=90d
```

## What It Does

**Strategic Optimization:**
1. Analyzes historical shipping data
2. Identifies patterns and inefficiencies
3. Sequential-thinking performs 15-20 thought analysis:
   - Cost patterns
   - Carrier performance
   - Route optimization
   - Volume trends
   - Seasonal factors
4. Provides actionable recommendations
5. Estimates cost/time savings

## MCP Integration

**Stage 1 - Data Analysis** (analytics-deep):
- Fetches historical metrics
- Aggregates by carrier, route, time
- Identifies anomalies
- Time: 5-8s

**Stage 2 - Strategic Thinking** (Sequential-thinking):
- Thought 1-5: Pattern identification
- Thought 6-10: Root cause analysis
- Thought 11-15: Solution brainstorming
- Thought 16-20: Recommendation prioritization
- Time: 10-15s

**Stage 3 - Context Enhancement** (Context7, optional):
- Industry best practices
- Carrier optimization strategies
- Time: 3-5s (cached)

## Output Format

```
🎯 Shipping Optimization Analysis (Last 30 Days)

📊 Current State:
- Total shipments: 1,247
- Total cost: $10,582.40
- Average cost: $8.48
- Delivery success: 94.2%

🧠 AI Strategic Analysis (Sequential-thinking):

Thought 1: Data shows 62% USPS dominance
→ Indicates lightweight inventory (<2 lbs)

Thought 2: Zero usage of USPS First Class
→ Missing cost-saving opportunity

Thought 3: FedEx usage at 26% seems high
→ Need to analyze weight distribution

Thought 4: 245 shipments to New York (20%)
→ Route concentration = negotiation leverage

Thought 5: Week-over-week 8.2% growth
→ Volume threshold for bulk discounts approaching

Thought 6: 782 USPS Priority packages
→ 23% are <1 lb and non-urgent

Thought 7: First Class saves $3-4 per package
→ 180 packages × $3.50 = $630/month

Thought 8: FedEx Ground used for 327 packages
→ 87 are <3 lbs (could use USPS)

Thought 9: LA → NY route could be optimized
→ USPS Regional Rate Box saves $1-2

Thought 10: Seasonal patterns not analyzed
→ Need holiday volume planning

Thought 11: Carrier mix can be optimized
→ Weight-based routing rules needed

Thought 12: Bulk discounts available at 1500/month
→ On track to reach in 6-8 weeks

Thought 13: Address validation saves 2% failures
→ Worth implementing ($212/month saved)

Thought 14: Saturday delivery rarely needed
→ Can use cheaper non-urgent options

Thought 15: Insurance overuse detected
→ 342 packages <$50 value with $100 insurance

Key Insight: Focus on automation rules for carrier selection

💡 Top 5 Recommendations:

1. Implement Weight-Based Routing Rules
   Priority: HIGH
   Impact: $630/month savings

   Action:
   - <1 lb + non-urgent → USPS First Class
   - 1-3 lbs + residential → USPS Priority
   - 3-10 lbs → Compare FedEx/UPS Ground
   - >10 lbs → FedEx/UPS Ground

   Implementation:
   - Add routing logic to create_shipment()
   - Update /bulk-create command with rules
   - Test with 10 sample shipments

   Expected Results:
   - 180 packages/month switch to First Class
   - Cost: $10,582 → $9,952 (6% reduction)
   - Delivery time: Same (3-5 days acceptable)
   - Timeline: 2 days to implement

2. Negotiate USPS Bulk Rate (LA → NY)
   Priority: MEDIUM
   Impact: $200-300/month savings

   Action:
   - Contact USPS for bulk pricing
   - Highlight: 245 shipments/month to NY
   - Request: 10-15% discount

   Leverage:
   - 20% of total volume
   - Consistent route
   - Growing 8% week-over-week

   Expected Results:
   - $8.50 → $7.20 per package
   - $1.30 × 245 = $318/month savings
   - Timeline: 1-2 weeks negotiation

3. Optimize FedEx Usage
   Priority: MEDIUM
   Impact: $305/month savings

   Action:
   - Identify 87 FedEx packages <3 lbs
   - Switch to USPS Priority ($5.50 cheaper)
   - Reserve FedEx for >3 lbs or urgent

   Implementation:
   - Update carrier selection rules
   - Add weight threshold check
   - Test with historical data

   Expected Results:
   - 87 packages × $5.50 = $478 savings
   - Some offset by higher USPS volume
   - Net savings: ~$305/month
   - Timeline: 3 days to implement

4. Implement Address Validation
   Priority: MEDIUM
   Impact: $212/month + fewer issues

   Action:
   - Add EasyPost address verification
   - Pre-validate before shipment creation
   - Auto-correct common errors

   Benefits:
   - Reduce 2% failure rate to 0.5%
   - Save 20 failed shipments/month
   - Cost: 20 × $10.60 = $212/month
   - Better customer experience

   Implementation:
   - Add verify_address() call
   - Update /bulk-create validation
   - Timeline: 1 day

5. Prepare for Bulk Discount Tier
   Priority: LOW (plan ahead)
   Impact: $1,270/month at scale

   Action:
   - Track: Currently 1,247/month
   - Target: 1,500/month (USPS bulk tier)
   - Growth: 8.2% WoW = 6 weeks to target

   Plan:
   - Month 1: Reach 1,500 threshold
   - Month 2: Negotiate 12% bulk discount
   - Month 3: Realize savings

   Expected Results:
   - 12% on $10,582 = $1,270/month
   - Requires no process changes
   - Timeline: 2-3 months

📊 Optimization Summary:

Total Monthly Savings: $1,450 (13.7%)

Implementation Timeline:
- Week 1: Rules + address validation
- Week 2: FedEx optimization
- Month 1: USPS negotiation
- Month 2-3: Bulk discount tier

Cost Breakdown:
- Current: $10,582/month
- After optimization: $9,132/month
- Savings: $1,450/month ($17,400/year)

No service degradation expected
All changes reversible
Automated implementation possible

💼 Business Impact:

Monthly:
- 13.7% cost reduction
- Same delivery performance
- Better reliability (address validation)
- Reduced manual decisions

Annually:
- $17,400 savings
- Better carrier relationships
- Data-driven decision making
- Scalable processes

🎯 Next Steps:

Immediate (This Week):
1. Run: /bulk-create with new routing rules
2. Test: 10 sample shipments
3. Monitor: Cost and delivery times

Short-term (This Month):
1. Contact USPS for bulk pricing
2. Implement address validation
3. Update /carrier-compare defaults

Long-term (Next Quarter):
1. Track to 1,500/month volume
2. Negotiate bulk discounts
3. Automate seasonal planning

📈 Success Metrics:

Track monthly:
- Average cost per shipment (<$8.00 target)
- Failure rate (<0.5% target)
- USPS First Class usage (15-20% target)
- FedEx usage (15-18% target)

🔄 Continuous Optimization:

Run this command monthly:
/shipping-optimize

Updates recommendations based on:
- New data patterns
- Seasonal changes
- Volume growth
- Carrier performance
```

## AI Reasoning Quality

**Sequential-thinking provides:**
- Step-by-step analysis (15-20 thoughts)
- Pattern recognition from data
- Root cause identification
- Solution brainstorming
- Priority ranking with confidence scores

**Better than simple analytics because:**
- Considers interdependencies
- Identifies non-obvious patterns
- Provides strategic context
- Ranks by business impact
- Includes implementation details

## Related Commands

```bash
/analytics-deep 30d        # Get data for optimization
/shipping-optimize         # Strategic recommendations (this)
/carrier-compare [route]   # Apply optimizations
/bulk-create [data]        # Use optimized rules
```

**Strategic shipping optimization - AI-powered business intelligence!**

