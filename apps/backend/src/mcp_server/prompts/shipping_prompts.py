"""Standard shipping workflow prompts."""


def register_shipping_prompts(mcp):
    """Register shipping workflow prompts."""

    @mcp.prompt()
    def shipping_workflow(origin: str, destination: str) -> str:
        """Standard shipping workflow prompt."""
        return f"""Help me ship a package from {origin} to {destination}.

    Please:
    1. Get available rates
    2. Compare carrier options
    3. Create the shipment with the best rate
    4. Provide tracking information"""
