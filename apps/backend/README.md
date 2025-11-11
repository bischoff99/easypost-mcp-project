# EasyPost MCP Backend

FastAPI backend server with MCP (Model Context Protocol) integration for EasyPost shipping operations.

## Tech Stack

- **Python**: 3.10+
- **Framework**: FastAPI
- **MCP**: FastMCP 2.0+
- **API**: EasyPost SDK
- **Testing**: pytest with asyncio support
- **Performance**: uvloop, ThreadPoolExecutor
- **Linting**: ruff, black, mypy

## Quick Start

### Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp ../.env.example ../.env
# Edit ../.env with your EasyPost test API key
```

### Running

```bash
# Development (uses root .env)
uvicorn src.server:app --reload

# Production
ENVIRONMENT=production uvicorn src.server:app --workers 33

# Health check
curl http://localhost:8000/health
```

## Project Structure

```
backend/
├── src/
│   ├── server.py              # FastAPI HTTP server
│   ├── mcp/
│   │   ├── __init__.py        # MCP server initialization
│   │   ├── tools/             # MCP tools (callable functions)
│   │   ├── resources/         # MCP resources (data providers)
│   │   └── prompts/           # MCP prompts (AI templates)
│   ├── services/
│   │   ├── easypost_service.py   # EasyPost API wrapper
│   │   └── smart_customs.py      # Smart customs info generation
│   ├── models/                # Pydantic models
│   ├── utils/                 # Utilities (config, monitoring)
│   └── exceptions/            # Custom exceptions
├── tests/
│   ├── unit/                  # Unit tests (mocked)
│   ├── integration/           # Integration tests (real API)
│   └── conftest.py           # Pytest fixtures
├── pytest.ini                 # Test configuration
└── requirements.txt          # Python dependencies
```

## Testing

### Run All Tests

```bash
# All tests with 16 parallel workers (M3 Max optimized)
pytest tests/ -v

# Unit tests only (fast)
pytest tests/unit/ -v

# Integration tests (requires EASYPOST_API_KEY env var)
pytest tests/integration/ -v -m integration

# With coverage
pytest tests/ -v --cov=src --cov-report=html
# View: open htmlcov/index.html
```

### Run Specific Tests

```bash
# Single test file
pytest tests/unit/test_bulk_tools.py -v

# Single test function
pytest tests/unit/test_bulk_tools.py::TestBulkToolsParsing::test_parse_dimensions_standard -v

# Tests matching pattern
pytest tests/ -k "bulk" -v
```

### Performance Benchmarks

```bash
# Run performance benchmarks
pytest tests/integration/test_bulk_performance.py -v

# Or use the script
cd .. && ./scripts/benchmark.sh
```

## Code Quality

### Linting

```bash
# Check code
ruff check src/ tests/

# Auto-fix
ruff check src/ tests/ --fix

# Format
black src/ tests/

# Type check
mypy src/
```

### Pre-commit Hooks

Pre-commit hooks run automatically on `git commit`:

- ruff (linting)
- black (formatting)
- prettier (markdown/json)

## API Endpoints

### FastAPI HTTP Server

- **GET** `/` - Server info
- **GET** `/health` - Health check with EasyPost API validation
- **GET** `/metrics` - Performance metrics
- **POST** `/rates` - Get shipping rates
- **POST** `/shipments` - Create shipment
- **GET** `/shipments` - List shipments
- **GET** `/shipments/{id}` - Get shipment details
- **GET** `/tracking/{number}` - Track package
- **GET** `/analytics` - Analytics dashboard (parallel processing)

View interactive docs: http://localhost:8000/docs

### MCP Server

The MCP server exposes tools for Claude Desktop integration:

**Tools:**

- `create_shipment` - Create single shipment
- `create_bulk_shipments` - Parallel bulk creation (16 workers)
- `track_shipment` - Track by tracking number
- `batch_track_shipments` - Track multiple packages
- `get_rates` - Compare shipping rates

**Resources:**

- `shipment://list` - Recent shipments
- `stats://summary` - Analytics overview

**Prompts:**

- Shipping optimization suggestions
- Carrier comparison analysis
- Package tracking assistance

## Configuration

### Environment Variables

```bash
# Required
EASYPOST_API_KEY=your_api_key_here

# Optional
MCP_HOST=0.0.0.0
MCP_PORT=8000
MCP_LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:5173
ENVIRONMENT=development  # or production
```

See `../.env.example` for full list.

### Hardware Optimization

The backend is optimized for M3 Max (16 cores) but adapts to available hardware:

- **ThreadPoolExecutor**: `min(40, cpu_count * 2)` workers
- **Bulk operations**: 16-32 parallel workers
- **Analytics**: 16-chunk parallel processing
- **uvloop**: 2-4x async I/O performance boost

## Performance

### Expected Throughput (M3 Max)

- Bulk shipment creation: **3-4 shipments/second**
- Batch tracking: **50 packages in 2-3s** (16x speedup)
- Analytics: **1000 shipments in 1-2s** (10x speedup)
- Test execution: **16 parallel workers**

### Optimization Techniques

- uvloop for faster async I/O
- ThreadPoolExecutor for EasyPost API calls
- asyncio.gather for concurrent operations
- Chunk-based parallel processing
- Smart customs caching (95%+ hit rate)

## Development

### Adding a New MCP Tool

1. Create tool function in `src/mcp/tools/new_tool.py`:

```python
def register_new_tools(mcp, easypost_service):
    @mcp.tool()
    async def my_new_tool(param: str) -> dict:
        """Tool description for AI."""
        # Implementation
        return {"status": "success"}
```

2. Register in `src/mcp/tools/__init__.py`:

```python
from src.mcp.tools.new_tool import register_new_tools

def register_tools(mcp, easypost_service):
    # ... existing registrations
    register_new_tools(mcp, easypost_service)
```

3. Add tests in `tests/unit/test_new_tool.py`

### Adding a New API Endpoint

1. Add route in `src/server.py`:

```python
@app.post("/my-endpoint")
@limiter.limit("10/minute")
async def my_endpoint(request: Request, data: MyModel):
    request_id = getattr(request.state, "request_id", "unknown")
    try:
        # Implementation
        return {"status": "success"}
    except Exception as e:
        logger.error(f"[{request_id}] Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
```

2. Create Pydantic model in `src/models/`
3. Add tests in `tests/unit/`

## Development Setup

### Dependencies

This project uses a two-file dependency system:

- `requirements.in` - Core dependencies (human-edited)
- `requirements-lock.txt` - Locked versions (generated via `pip freeze`)
- `requirements.txt` - Legacy compatibility (kept for backwards compatibility)

**Installing dependencies:**

```bash
pip install -r requirements-lock.txt
```

**Updating dependencies:**

```bash
# 1. Edit requirements.in
# 2. Install updated packages
pip install -r requirements.in
# 3. Regenerate lock file
pip freeze > requirements-lock.txt
```

**Note**: `pip-compile` not used due to Python 3.14 compatibility issues. Use `pip freeze` instead.

## Troubleshooting

### Common Issues

**Import errors:**

```bash
# Make sure virtual environment is activated
source venv/bin/activate
# Reinstall dependencies
pip install -r requirements.txt
```

**EasyPost API errors:**

```bash
# Verify API key
python -c "import os; from dotenv import load_dotenv; load_dotenv('../.env'); print(os.getenv('EASYPOST_API_KEY'))"
# Should print your API key starting with EZTK (test) or EZAK (production)
```

**Tests failing:**

```bash
# Integration tests need API key
export EASYPOST_API_KEY=your_test_key
pytest tests/integration/ -v
```

**Performance issues:**

```bash
# Check worker configuration
python -c "import multiprocessing; print(f'CPU cores: {multiprocessing.cpu_count()}')"
```

## Contributing

1. Run tests: `pytest tests/ -v`
2. Run linters: `ruff check src/ && black src/`
3. Check types: `mypy src/`
4. All checks pass: `make check` (from root)

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [EasyPost API Docs](https://www.easypost.com/docs/api)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [pytest Documentation](https://docs.pytest.org/)
