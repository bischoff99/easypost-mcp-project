Generate a complete API endpoint for {{path}} with {{method}} method.

Read .dev-config.json for:
- Backend: FastAPI (Python 3.12)
- Testing: pytest with xdist (16 parallel workers)
- Conventions: snake_case functions, PascalCase classes
- Hardware: M3 Max (16 cores, 128GB RAM)

Generate:
1. Pydantic models (request/response) with Field validation
2. @app.{{method}}("{{path}}") async route handler
3. Error handling, logging, validation
4. Comprehensive pytest tests (success, validation, edge cases)
5. Optimize for parallel execution (pytest -n 16)

Use ThreadPoolExecutor with min(32, cpu_count * 2) workers.
Return standardized {"status": "success/error", "data": {}, "message": ""} format.