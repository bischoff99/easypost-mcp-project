"""MCP Prompts registration."""

from src.mcp_server.prompts.comparison_prompts import register_comparison_prompts
from src.mcp_server.prompts.optimization_prompts import register_optimization_prompts
from src.mcp_server.prompts.shipping_prompts import register_shipping_prompts
from src.mcp_server.prompts.tracking_prompts import register_tracking_prompts


def register_prompts(mcp):
    """Register all MCP prompts with the server."""
    register_shipping_prompts(mcp)
    register_comparison_prompts(mcp)
    register_tracking_prompts(mcp)
    register_optimization_prompts(mcp)
