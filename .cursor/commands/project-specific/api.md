> Global-scope caution: Preview by default; requires backend detection and explicit --apply to write files.

Generate a complete API endpoint for {{path}} with {{method}} method.

## Usage

```bash
/api {{path}} {{method}}           # Preview only (no writes)
/api {{path}} {{method}} --apply   # Generate files (requires {{stack.backend.framework}})
```

Read .dev-config.json for:

- Backend: FastAPI (Python 3.12)
- Testing: pytest with xdist (auto-detected workers)
- Conventions: snake_case functions, PascalCase classes
- Hardware: Auto-detected (max 16 workers per project constraints)

Generate:

1. Pydantic models (request/response) with Field validation
2. @app.{{method}}("{{path}}") async route handler
3. Error handling, logging, validation
4. Comprehensive pytest tests (success, validation, edge cases)
5. Optimize for parallel execution (pytest -n auto)

Use ThreadPoolExecutor with auto-detected workers (max 16 per project constraints).
Return standardized {"status": "success/error", "data": {}, "message": ""} format.
