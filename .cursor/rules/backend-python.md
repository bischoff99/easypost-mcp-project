# Backend Code Generation Rules

## Python Type Hints

Always include type hints for function parameters and returns.

Example:

```python
def fetch_shipment(shipment_id: str) -> ShipmentData:
    """Fetch shipment from EasyPost API."""
    pass
```

## Error Handling

- Use custom exceptions from `services.exceptions`
- Wrap external API calls in try-except blocks
- Log errors with context before re-raising
- Never silently fail on database operations

## Database Operations

- Use connection pooling (psycopg pool configured in `config.py`)
- All queries must be parameterized (prevent SQL injection)
- Import models from `src.models`, never raw SQL
- Use SQLAlchemy ORM when possible

## Async/Await Patterns

- Use `asyncio` for concurrent operations
- Prefix async functions with `async def`
- Always await external I/O (database, HTTP, MCP calls)

## Testing Patterns

- Write test function names as `test_<function>_<scenario>`
- Use pytest fixtures for common setup
- Mock EasyPost client: `@pytest.fixture def mock_easypost():`
- Include docstrings explaining test intent

## Import Organization

Use isort with project configuration:

```
from typing import ...  # stdlib
import asyncio         # stdlib

from sqlalchemy import ...  # third-party
import pytest

from src.models import ...  # local
from src.services import ...
```
