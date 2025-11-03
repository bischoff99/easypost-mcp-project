# AI Code Generation Templates

These templates speed up code generation by providing standard patterns.

## Usage in Cursor/AI Chat

Reference templates in prompts:
```
"Use @.ai-templates/api-endpoint.py for create_webhook endpoint"
"Copy @.ai-templates/react-component.jsx pattern for UserCard"
```

## Available Templates

### Backend
- `api-endpoint.py` - FastAPI endpoint with full error handling
- `mcp-tool.py` - FastMCP tool definition
- `pydantic-model.py` - Validated data model
- `pytest-test.py` - Test suite with fixtures

### Frontend
- `react-component.jsx` - React functional component
- `react-page.jsx` - Full page component with routing
- `custom-hook.js` - React custom hook
- `vitest-test.jsx` - Component test suite

## Quick Commands

Define these in your prompts:

- `/api [name]` - Create API endpoint from template
- `/tool [name]` - Create MCP tool from template
- `/component [name]` - Create React component
- `/hook [name]` - Create custom hook
- `/test [file]` - Generate tests for file
