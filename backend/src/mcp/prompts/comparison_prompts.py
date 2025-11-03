"""Carrier comparison prompts."""


def register_comparison_prompts(mcp):
    """Register carrier comparison prompts."""

    @mcp.prompt()
    def compare_carriers(
        origin: str,
        destination: str,
        weight_oz: float,
        length: float,
        width: float,
        height: float,
    ) -> str:
        """Compare shipping rates across all available carriers."""
        return f"""Help me compare shipping costs from {origin} to {destination}.

Package details:
- Weight: {weight_oz} oz
- Dimensions: {length} x {width} x {height} inches

Please:
1. Use get_rates tool to fetch rates from USPS, FedEx, and UPS
2. Compare prices, delivery times, and service levels
3. Create a comparison table showing:
   - Carrier name
   - Service type
   - Price
   - Estimated delivery time
4. Recommend the best option based on:
   - Lowest cost
   - Fastest delivery
   - Best value (cost vs speed)"""

    @mcp.prompt()
    def bulk_rate_check(origin: str, destinations: str, weight_oz: float) -> str:
        """Check rates for shipping to multiple destinations."""
        return f"""Check shipping rates from {origin} to multiple destinations.

Package details:
- Weight: {weight_oz} oz
- Standard box dimensions (12 x 9 x 6 inches)

Destinations: {destinations}

Please:
1. For each destination, get USPS rates (most economical for bulk)
2. Create a summary table showing:
   - Destination
   - USPS Ground price
   - USPS Priority price
   - Estimated delivery time
3. Calculate total cost for all shipments
4. Identify any bulk discount opportunities"""
