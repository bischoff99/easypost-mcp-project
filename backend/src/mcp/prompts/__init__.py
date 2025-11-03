"""MCP Prompts registration."""

from src.mcp.prompts.shipping_prompts import register_shipping_prompts
from src.mcp.prompts.comparison_prompts import register_comparison_prompts
from src.mcp.prompts.tracking_prompts import register_tracking_prompts
from src.mcp.prompts.optimization_prompts import register_optimization_prompts


def register_prompts(mcp):
    """Register all MCP prompts with the server."""
    register_shipping_prompts(mcp)
    register_comparison_prompts(mcp)
    register_tracking_prompts(mcp)
    register_optimization_prompts(mcp)

