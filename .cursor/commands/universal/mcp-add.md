Scaffold a new MCP tool with complete boilerplate code.

**Arguments**: `/mcp-add [tool-name] [type]`
- `tool-name`: Name of the tool (e.g., "email", "analytics")
- `type`: `tool` | `prompt` | `resource` (defaults to "tool")

## What It Generates

**Complete MCP Tool Structure:**
1. Tool/Prompt/Resource file with boilerplate
2. Type definitions and validation
3. Registration in `__init__.py`
4. Unit tests with mocks
5. Integration tests
6. README with usage examples
7. Error handling patterns

## MCP Tool Types

### Type: `tool` (Most common)
**Generates**: Executable function that performs actions

**Example**: `/mcp-add email-notify tool`

Creates `backend/src/mcp/tools/email_notify_tools.py`:
```python
"""Email notification MCP tool."""
import logging
from typing import Any, Dict
from fastmcp import Context

logger = logging.getLogger(__name__)

def register_email_notify_tools(mcp, service):
    """Register email notification tools."""

    @mcp.tool()
    async def send_email_notification(
        to_address: str,
        subject: str,
        body: str,
        ctx: Context = None
    ) -> Dict[str, Any]:
        """Send email notification.

        Args:
            to_address: Recipient email
            subject: Email subject
            body: Email body text
            ctx: MCP context for progress reporting

        Returns:
            Status and message
        """
        try:
            if ctx:
                await ctx.info(f"Sending email to {to_address}...")

            # Your implementation here
            result = await service.send_email(to_address, subject, body)

            if ctx:
                await ctx.report_progress(1, 1)

            return {
                "status": "success",
                "message": f"Email sent to {to_address}",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }

        except Exception as e:
            logger.error(f"Email notification failed: {str(e)}")
            return {
                "status": "error",
                "message": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
```

### Type: `prompt`
**Generates**: Predefined conversation starters

**Example**: `/mcp-add shipping-compare prompt`

Creates `backend/src/mcp/prompts/shipping_compare_prompts.py`

### Type: `resource`
**Generates**: Data providers (read-only)

**Example**: `/mcp-add shipment-history resource`

Creates `backend/src/mcp/resources/shipment_history_resources.py`

## MCP Integration

**Stage 1 - Get Best Practices** (Context7):
- Library: `/fastapi/fastapi` (or detected framework)
- Topic: "MCP server tools async patterns validation"
- Tokens: 5000
- Cache: 24h

**Stage 2 - Generate Structure** (Desktop Commander):
- Create: Directory if not exists
- Write: Tool file with boilerplate
- Update: `__init__.py` registration
- Generate: Test file

**Stage 3 - Verify** (Desktop Commander):
- Check: Syntax is valid
- Run: `pytest tests/unit/test_{{tool_name}}.py`
- Report: Generated files and next steps

## Generated File Structure

```
backend/src/mcp/
├── tools/
│   └── email_notify_tools.py       # Generated tool
├── __init__.py                      # Updated with registration
│
backend/tests/unit/
└── test_email_notify_tools.py      # Generated tests
```

## Boilerplate Includes

**All tool files include:**
- Proper async/await patterns
- Type hints (Dict, Any, Optional)
- Error handling (try/except with logging)
- Progress reporting (ctx.info, ctx.report_progress)
- Validation (Pydantic models if needed)
- Logging with context
- Standardized response format
- Docstrings (Google style)

**All test files include:**
- Fixtures for service mocks
- Success case tests
- Error case tests
- Validation tests
- pytest markers (@pytest.mark.asyncio)
- Mock MCP context

## Auto-Detection from Config

Reads `.dev-config.json`:
```json
{
  "paths": {
    "backend": "backend/src",
    "mcp": {
      "tools": "backend/src/mcp/tools",
      "prompts": "backend/src/mcp/prompts",
      "resources": "backend/src/mcp/resources"
    }
  },
  "conventions": {
    "python": {
      "functions": "snake_case",
      "files": "snake_case.py"
    }
  }
}
```

Automatically:
- Uses correct paths for your project
- Applies naming conventions
- Imports correct service from your codebase
- Matches your code style

## Usage Examples

```bash
# Generate MCP tool
/mcp-add email-notify tool

# Generate MCP prompt
/mcp-add rate-comparison prompt

# Generate MCP resource
/mcp-add shipment-stats resource

# With service integration
/mcp-add sms-alert tool --service=NotificationService
```

## Output

```
🛠️ Generating MCP Tool: email-notify (type: tool)

📚 Best Practices (Context7):
- Loaded FastAPI MCP patterns
- Using async/await patterns
- Standardized error handling

📝 Generated Files:
✅ backend/src/mcp/tools/email_notify_tools.py (87 lines)
✅ backend/tests/unit/test_email_notify_tools.py (124 lines)
✅ Updated backend/src/mcp/__init__.py (registration)

🧪 Verification:
Running: pytest backend/tests/unit/test_email_notify_tools.py -v
Result: ✅ 4/4 tests passed

✅ MCP Tool Ready!

Next steps:
1. Implement business logic in send_email_notification()
2. Add service integration if needed
3. Test with: /test backend/tests/unit/test_email_notify_tools.py
4. Use in MCP client: call send_email_notification()
```

## Template Customization

Adapts template based on:
- **Language**: Python, JavaScript, Go (from config)
- **Framework**: FastAPI, Django, Express (from config)
- **Async patterns**: async/await, promises, goroutines
- **Type system**: Pydantic, Zod, structs
- **Testing**: pytest, vitest, go test

## Naming Conventions

**Automatically applies from config:**
- Python: `snake_case` functions, `PascalCase` classes
- JavaScript: `camelCase` functions, `PascalCase` components
- Go: `PascalCase` exported, `camelCase` private
- File names: Match language conventions

## Integration Pattern

**Generates registration code:**
```python
# In backend/src/mcp/__init__.py
from src.mcp.tools import register_email_notify_tools

# Register all MCP components
register_tools(mcp, easypost_service)
register_email_notify_tools(mcp, notification_service)  # Added
```

## Advanced Options

```bash
# With specific service
/mcp-add analytics tool --service=AnalyticsService

# With dependencies
/mcp-add pdf-generator tool --deps=reportlab,pillow

# Skip tests (faster generation)
/mcp-add quick-tool tool --no-tests

# Generate multiple types
/mcp-add shipping tool,prompt,resource
```

## Performance

- Template generation: 2-3s
- Context7 lookup: 3-5s (cached 24h)
- File creation: 1-2s
- Test generation: 2-3s
- Verification: 3-5s
- **Total: 10-15s** for complete scaffold

## Adapts To Any MCP Server

Works with:
- FastMCP (Python)
- @modelcontextprotocol/sdk (TypeScript)
- mcp-go (Go)
- Any MCP-compliant server

Detects from project structure and generates appropriate code.

**Scaffold new MCP tools in seconds, not hours.**

