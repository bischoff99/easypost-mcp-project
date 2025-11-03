# Exa Research Findings - EasyPost MCP Project

Research conducted: November 3, 2025

## Overview

Used Exa web search to find latest information about:
1. cursor.directory MCP servers
2. FastMCP implementation patterns  
3. MCP tool design best practices
4. EasyPost Python/FastAPI integration

## Key Findings

### 1. cursor.directory Ecosystem

**Source**: [cursor.directory](https://cursor.directory), [Firecrawl Blog](https://www.firecrawl.dev/blog/best-mcp-servers-for-cursor)

**Stats**:
- 61.7k+ active members
- Featured MCP servers directory
- Job board with $215k-$275k positions for AI Agent Engineers

**Featured MCPs Discovered**:
1. **Postmark MCP** - Transactional email integration
2. **Postman MCP** - API testing integration
3. **Midday** - Finance/time tracking
4. **GibsonAI** - AI tooling
5. **Agent Evals by Galileo** - AI agent evaluation
6. **Peekaboo** - macOS screenshots for agents
7. **Mailtrap Email Sending** - Email platform MCP

**Key Insight from Firecrawl Blog**:
> "MCP servers eliminate context switching. Developers using MCP servers report 40% fewer tool switches during coding sessions."

**Real-world benefits**:
- Direct database queries without leaving Cursor
- Web scraping for research while coding
- Browser automation for testing workflows
- Design asset access from Figma/Notion
- Version control operations through AI prompts

### 2. FastMCP Implementation Patterns

**Sources**: 
- [Medium - Manish Shivanandhan](https://medium.com/@manishmshiva/how-to-build-your-first-mcp-server-using-fastmcp-170873fb7f1e)
- [freeCodeCamp Tutorial](https://www.freecodecamp.org/news/how-to-build-your-own-mcp-server-with-python/)
- [The Python Code](https://thepythoncode.com/article/fastmcp-mcp-client-server-todo-manager)
- [Firecrawl - Complete FastMCP Tutorial](https://www.firecrawl.dev/blog/fastmcp-tutorial-building-mcp-servers-python)

#### Core FastMCP Architecture

**From The Python Code Tutorial - Todo Manager Example**:

FastMCP servers expose three component types:

1. **Tools**: Actions the client/LLM can execute (POST/PUT side-effects)
   - Examples: create_todo, complete_todo, search_todos
   
2. **Resources**: Read-only data sources (GET endpoints)
   - Examples: configuration, files, database records, metrics
   - URI-based: `stats://todos`, `config://settings`
   
3. **Prompts**: Reusable message templates
   - Structure LLM interactions
   - Guide agent behavior

**Transports Supported**:
- **stdio**: Local development (our current setup ✓)
- **HTTP**: Web services
- **SSE**: Server-sent events

#### Best Practices from freeCodeCamp Tutorial

**Tool Definition Pattern**:
```python
from fastmcp import FastMCP

mcp = FastMCP(
    name="Server Name",
    instructions="Clear description of what this server does"
)

@mcp.tool()
async def tool_name(param: str, ctx: Context = None) -> dict:
    """Tool description that AI can understand"""
    if ctx:
        await ctx.info("Status message")
    
    result = await perform_operation(param)
    
    return {
        "status": "success",
        "data": result,
        "message": "Operation completed"
    }
```

**Resource Pattern**:
```python
@mcp.resource("resource://identifier")
async def get_resource(uri: str) -> dict:
    """Resource description"""
    return {
        "data": fetch_data(),
        "metadata": {"type": "resource_type"}
    }
```

**Prompt Pattern**:
```python
@mcp.prompt()
def workflow_prompt(context: str) -> str:
    """Workflow description"""
    return f"""Guide the AI through:
    1. Step one
    2. Step two
    3. Step three
    
    Context: {context}
    """
```

#### Advanced Patterns from Firecrawl Tutorial

**Environment-Based Configuration**:
```python
import os
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP(
    name="Production Server",
    instructions="Server instructions"
)

# Use environment variables for sensitive data
API_KEY = os.getenv("API_KEY")
```

**Logging Configuration**:
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
```

**Testing Pattern**:
```python
# Test your MCP server programmatically
from fastmcp import create_client

async def test_server():
    async with create_client() as client:
        tools = await client.list_tools()
        result = await client.call_tool("tool_name", {"param": "value"})
        assert result["status"] == "success"
```

### 3. MCP Tool Design & Error Handling

**Sources**:
- [MCP Official Docs - Tools](https://modelcontextprotocol.info/docs/concepts/tools/)
- [MCPcat - Error Handling Guide](https://mcpcat.io/guides/error-handling-custom-mcp-servers/)
- [Docker Blog - MCP Misconceptions](https://www.docker.com/blog/mcp-misconceptions-tools-agents-not-api/)
- [ZBrain - MCP Deep Dive](https://zbrain.ai/model-context-protocol/)

#### Tool Definition Structure (Official MCP Spec)

```typescript
{
  name: string;              // Unique identifier
  description?: string;      // Human-readable description
  inputSchema: {            // JSON Schema for parameters
    type: "object",
    properties: { ... }     // Tool-specific parameters
  }
}
```

**Key Principle from Docker Blog**:
> "MCP is not an API. Tools are not agents. MCP is more than tools."

**Critical Insights**:
1. **MCP ≠ API**: It's a model-facing protocol for LLM tool use
2. **Intent Mediation**: Tools carry intent and affordances, not just endpoints
3. **Context Surfaces**: Beyond request/response - prompts, elicitations, resources
4. **Deterministic Last Mile**: Tool execution should be deterministic and idempotent

#### Error Handling Best Practices (MCPcat Guide)

**Three-Tier Error Model**:

1. **Transport-Level Errors**:
   - Network timeouts, broken pipes, auth failures
   - Handled by transport layer (stdio, HTTP, SSE)

2. **Protocol-Level Errors**:
   - JSON-RPC violations
   - Malformed JSON, non-existent methods, invalid parameters
   
```python
{
    "jsonrpc": "2.0",
    "id": "request-123",
    "error": {
        "code": -32601,
        "message": "Method not found",
        "data": "The method 'unknown_tool' does not exist"
    }
}
```

3. **Application-Level Errors**:
   - Business logic failures
   - External API errors
   
**Recommended Pattern**:
```python
@mcp.tool()
async def handle_tool(name: str, arguments: dict):
    try:
        result = await process_tool(name, arguments)
        return CallToolResult(
            content=[TextContent(text=str(result))]
        )
    except ValidationError as e:
        return CallToolResult(
            isError=True,
            content=[TextContent(text=f"Validation error: {str(e)}")]
        )
    except ExternalAPIError as e:
        return CallToolResult(
            isError=True,
            content=[TextContent(text=f"External service error: {str(e)}")]
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return CallToolResult(
            isError=True,
            content=[TextContent(text="An unexpected error occurred")]
        )
```

**Why This Matters**:
- Prevents server crashes
- Helps LLMs understand failures
- Enables retry logic
- Allows user intervention when needed

#### Design Anti-Patterns to Avoid

From Docker Blog:

❌ **Don't**:
- Treat MCP tools as business APIs with complex state changes
- Expect strict schema obedience from AI models
- Build MCP tools that mutate state without validation

✅ **Do**:
- Keep stable business APIs separate
- Wrap them with MCP tool definitions
- Express preconditions and success criteria
- Make tools deterministic and idempotent
- Validate inputs from model planning
- Fail closed with clear error messages

### 4. EasyPost API Integration Patterns

**Sources**:
- [EasyPost Python SDK - GitHub](https://github.com/EasyPost/easypost-python)
- [EasyPost Getting Started - Python](https://www.easypost.com/getting-started/python)
- [EasyPost Tracking Guide](https://www.easypost.com/tracking-guide/python)
- [EasyPost Tracking API](https://www.easypost.com/tracking-api/)

#### Official EasyPost Python SDK

**Installation**:
```bash
pip install easypost>=10.0.0
```

**Basic Usage Pattern**:
```python
import easypost

# Setup client
easypost.api_key = "YOUR_API_KEY"

# Create shipment
shipment = easypost.Shipment.create(
    to_address={
        "name": "Jane Doe",
        "street1": "123 Main St",
        "city": "San Francisco",
        "state": "CA",
        "zip": "94102",
        "country": "US"
    },
    from_address={
        "name": "John Smith",
        "street1": "456 Oak Ave",
        "city": "New York",
        "state": "NY",
        "zip": "10001",
        "country": "US"
    },
    parcel={
        "length": 10,
        "width": 8,
        "height": 5,
        "weight": 2
    }
)

# Buy label
rate = shipment.lowest_rate("USPS")
shipment.buy(rate=rate)
```

#### Tracking Integration

**Two Methods**:

1. **With Existing Tracking Number**:
```python
tracker = easypost.Tracker.create(
    tracking_code="EZ1000000001",
    carrier="USPS"  # Optional - auto-detects if omitted
)
```

2. **Automatic with Label Purchase**:
   - Every EasyPost shipment includes free tracker
   - Automatically created when label is purchased

**Tracker Response Format**:
```python
{
    "id": "trk_...",
    "tracking_code": "EZ1000000001",
    "carrier": "USPS",
    "status": "pre_transit",
    "est_delivery_date": "2020-02-08T21:39:12Z",
    "status_detail": "status_update",
    "is_return": false,
    "public_url": "https://track.easypost.com/...",
    "tracking_details": [
        {
            "datetime": "2020-02-08T21:39:12Z",
            "status": "pre_transit",
            "message": "Label created",
            "tracking_location": {
                "city": "New York",
                "state": "NY",
                "country": "US"
            }
        }
    ]
}
```

#### Webhook Integration (From Tracking Guide)

**Setup**:
1. Configure webhook URLs in EasyPost Dashboard
2. Set for both Test and Production modes
3. Receive automatic updates on package movements

**Events**:
- Package status changes
- Delivery updates
- Exception notifications
- Tracking updates

**Webhook Pattern**:
```python
from fastapi import Request

@app.post("/webhooks/tracking")
async def tracking_webhook(request: Request):
    payload = await request.json()
    
    # Verify webhook signature
    # Process tracking update
    # Notify customer
    
    return {"status": "received"}
```

## Comparison with Our Implementation

### ✅ What We're Doing Right

Based on research findings, our EasyPost MCP server already follows best practices:

1. **Tool Naming** ✓
   - `create_shipment`, `get_tracking`, `get_rates`
   - Follows verb_noun pattern
   - Clear, action-oriented

2. **Tool Descriptions** ✓
   - "Create a new shipment and purchase a label"
   - "Get real-time tracking information"
   - Clear and AI-understandable

3. **Error Handling** ✓
   - Standardized response format
   - Try-catch blocks
   - User-friendly error messages

4. **Type Hints** ✓
   - All parameters typed
   - Return types specified
   - Pydantic models for validation

5. **Async/Await** ✓
   - Proper async implementation
   - ThreadPoolExecutor for sync SDK
   - Non-blocking operations

6. **Environment Variables** ✓
   - API key in .env
   - Config validation
   - Separate test/production

### ⚠️ Improvements Needed

Based on research, we should add:

1. **Resources** (Missing)
```python
@mcp.resource("easypost://shipments/recent")
async def get_recent_shipments() -> dict:
    """List recent shipments"""
    return {
        "shipments": [...],
        "count": 10
    }

@mcp.resource("easypost://stats/overview")
async def get_stats() -> dict:
    """Get shipping statistics"""
    return {
        "total_shipments": 100,
        "total_spent": 1234.56
    }
```

2. **Enhanced Prompts**
```python
@mcp.prompt()
def shipping_workflow_v2(origin: str, destination: str) -> list:
    """Enhanced workflow with multiple messages"""
    return [
        {
            "role": "user",
            "content": f"I need to ship from {origin} to {destination}"
        },
        {
            "role": "assistant",
            "content": "I'll help you find the best shipping option."
        }
    ]
```

3. **Better Error Context**
```python
from fastmcp import CallToolResult, TextContent

@mcp.tool()
async def create_shipment_enhanced(...):
    try:
        result = await easypost_service.create_shipment(...)
        return CallToolResult(
            content=[TextContent(
                type="text",
                text=json.dumps(result)
            )]
        )
    except ValidationError as e:
        return CallToolResult(
            isError=True,
            content=[TextContent(
                type="text",
                text=f"Invalid input: {str(e)}. Please check address format."
            )]
        )
```

4. **Logging Enhancement**
```python
# Add structured logging
import logging
import json

logger = logging.getLogger(__name__)

@mcp.tool()
async def create_shipment(...):
    logger.info(f"Creating shipment", extra={
        "tool": "create_shipment",
        "carrier": carrier,
        "to_city": to_address.get("city")
    })
    # ... rest of implementation
```

5. **Progress Reporting**
```python
@mcp.tool()
async def create_shipment(..., ctx: Context = None):
    if ctx:
        await ctx.info("Validating addresses...")
    # ... validation
    
    if ctx:
        await ctx.info("Getting rates from carriers...")
    # ... get rates
    
    if ctx:
        await ctx.info("Purchasing label...")
    # ... purchase
    
    if ctx:
        await ctx.report_progress(1, 1)
```

## Recommended Next Steps

### Immediate (High Priority)

1. **Add MCP Resources** - 30 min
   - `easypost://shipments/recent`
   - `easypost://stats/overview`
   - `easypost://carriers/list`

2. **Enhance Error Handling** - 20 min
   - Use `CallToolResult` with `isError`
   - Add specific error types
   - Improve error messages

3. **Add Progress Reporting** - 15 min
   - Use `ctx.info()` for status updates
   - Use `ctx.report_progress()` for long operations

### Medium Priority

4. **Improve Logging** - 30 min
   - Structured JSON logging
   - Request/response tracking
   - Performance metrics

5. **Add More Prompts** - 20 min
   - Batch shipping workflow
   - Address validation workflow
   - Rate comparison workflow

6. **Testing Suite** - 1 hour
   - Programmatic MCP client tests
   - Mock EasyPost API responses
   - Integration tests

### Low Priority

7. **Add HTTP Transport** - 1 hour
   - Support both stdio and HTTP
   - Enable web-based clients

8. **Webhook Handler** - 1 hour
   - Add tracking update webhooks
   - Notify on delivery events

9. **Deployment Guide** - 30 min
   - Document cloud deployment
   - Docker containerization
   - Production configuration

## Resources & Links

### FastMCP Tutorials
- [Medium - Building First MCP Server](https://medium.com/@manishmshiva/how-to-build-your-first-mcp-server-using-fastmcp-170873fb7f1e)
- [freeCodeCamp - MCP Server Tutorial](https://www.freecodecamp.org/news/how-to-build-your-own-mcp-server-with-python/)
- [The Python Code - Todo Manager](https://thepythoncode.com/article/fastmcp-mcp-client-server-todo-manager)
- [Firecrawl - Complete Guide](https://www.firecrawl.dev/blog/fastmcp-tutorial-building-mcp-servers-python)

### MCP Best Practices
- [MCP Official Docs - Tools](https://modelcontextprotocol.info/docs/concepts/tools/)
- [MCPcat - Error Handling](https://mcpcat.io/guides/error-handling-custom-mcp-servers/)
- [Docker - MCP Misconceptions](https://www.docker.com/blog/mcp-misconceptions-tools-agents-not-api/)
- [ZBrain - MCP Deep Dive](https://zbrain.ai/model-context-protocol/)

### EasyPost Integration
- [EasyPost Python SDK](https://github.com/EasyPost/easypost-python)
- [Getting Started Guide](https://www.easypost.com/getting-started/python)
- [Tracking Guide](https://www.easypost.com/tracking-guide/python)
- [Tracking API Docs](https://www.easypost.com/tracking-api/)

### cursor.directory
- [Main Site](https://cursor.directory)
- [MCP Servers Directory](https://cursor.directory/mcp)
- [Community Board](https://cursor.directory/board)
- [Firecrawl - 15 Best MCP Servers](https://www.firecrawl.dev/blog/best-mcp-servers-for-cursor)

## Key Quotes

> "MCP servers eliminate context switching. Developers using MCP servers report 40% fewer tool switches during coding sessions." - Anthropic Data

> "MCP is not an API. Tools are not agents. MCP is more than tools." - Docker Blog

> "Building good MCP servers is legitimately difficult. It's not just wrapping your API in a different protocol. You have to think like an agent." - cursor.directory Community

> "MCP is the USB-C for AI - a consistent, secure JSON-RPC interface that lets any compliant AI client plug into any data or service source without bespoke code." - ZBrain

## Summary

Exa research revealed:

1. **cursor.directory** is the premier community (61.7k+ members) with featured MCP servers
2. **FastMCP** has comprehensive tutorials from multiple sources
3. **MCP best practices** emphasize deterministic tools, proper error handling, and context awareness
4. **EasyPost SDK** is mature and well-documented with tracking/webhook support

**Our EasyPost MCP** is well-structured but can be enhanced with:
- MCP Resources for read-only data
- Better error context with `isError` flag
- Progress reporting with Context
- Structured logging
- Additional workflow prompts

**Priority**: Add resources and improve error handling first (1 hour total work).
