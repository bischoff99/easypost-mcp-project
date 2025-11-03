"""Cost optimization prompts."""


def register_optimization_prompts(mcp):
    """Register cost optimization prompts."""

    @mcp.prompt()
    def cost_optimization(
        origin: str,
        destination: str,
        weight_oz: float,
        length: float,
        width: float,
        height: float,
        max_budget: float = None,
        max_days: int = None,
    ) -> str:
        """Find the most cost-effective shipping option with constraints."""
        constraints = []
        if max_budget:
            constraints.append(f"- Budget: ${max_budget} maximum")
        if max_days:
            constraints.append(f"- Delivery: {max_days} days maximum")

        constraints_text = "\n".join(constraints) if constraints else "- No constraints specified"

        return f"""Find the most cost-effective shipping option from {origin} to {destination}.

Package details:
- Weight: {weight_oz} oz
- Dimensions: {length} x {width} x {height} inches

Constraints:
{constraints_text}

Please:
1. Get rates from all available carriers
2. Filter options that meet the constraints
3. Rank by cost (lowest to highest)
4. Show top 3 options with pros/cons
5. Recommend the best value option with justification"""
