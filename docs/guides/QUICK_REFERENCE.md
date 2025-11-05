# Quick Reference: PostgreSQL & Proxy Patterns

**Fast lookup for common patterns in your EasyPost MCP project**

---

## PostgreSQL Patterns

### Which Pool to Use?

```python
# Use SQLAlchemy ORM (Depends(get_db))
✅ Single CRUD operations
✅ Relationships (shipment → address)
✅ Type-safe queries
✅ Pydantic serialization

# Use Direct asyncpg (app.state.db_pool)
✅ Bulk operations (100+ records)
✅ Analytics aggregations
✅ Raw SQL performance
✅ Parallel processing
```

---

## Code Templates

### 1. Simple CRUD (SQLAlchemy)

```python
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models import Shipment

@app.get("/shipments/{id}")
async def get_shipment(id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Shipment).where(Shipment.id == id)
    )
    return result.scalar_one_or_none()

@app.post("/shipments")
async def create_shipment(data: ShipmentCreate, db: AsyncSession = Depends(get_db)):
    shipment = Shipment(**data.dict())
    db.add(shipment)
    await db.commit()
    await db.refresh(shipment)
    return shipment
```

### 2. Bulk Operations (Direct asyncpg)

```python
@app.post("/shipments/batch-track")
async def batch_track(tracking_numbers: List[str], request: Request):
    pool = request.app.state.db_pool

    results = await pool.fetch(
        "SELECT * FROM shipments WHERE tracking_number = ANY($1)",
        tracking_numbers
    )

    return [dict(r) for r in results]
```

### 3. Service Layer (DatabaseService)

```python
from src.services.database_service import DatabaseService

@app.get("/analytics/{date}")
async def get_analytics(date: str, db: AsyncSession = Depends(get_db)):
    service = DatabaseService(db)
    summary = await service.get_analytics_summary_by_date(date)
    return summary
```

### 4. Rate Limited + DB Save

```python
@app.post("/shipments/bulk-create")
async def bulk_create(shipments: List[ShipmentCreate], request: Request):
    rate_limiter = request.app.state.rate_limiter
    db_pool = request.app.state.db_pool

    async def create_one(data):
        async with rate_limiter:  # 16 concurrent max
            ep_shipment = await easypost.create_shipment(data)

            async with db_pool.acquire() as conn:
                await conn.execute(
                    "INSERT INTO shipments (...) VALUES (...)",
                    ep_shipment.id, ...
                )

            return ep_shipment

    results = await asyncio.gather(*[create_one(s) for s in shipments])
    return {"created": len(results)}
```

---

## Connection Monitoring

### Check PostgreSQL Connections

```sql
-- Active connections
SELECT count(*) FROM pg_stat_activity WHERE datname = 'easypost';

-- By state
SELECT
    state,
    count(*)
FROM pg_stat_activity
WHERE datname = 'easypost'
GROUP BY state;

-- Pool health
SELECT
    count(*) as total,
    count(*) FILTER (WHERE state = 'active') as active,
    count(*) FILTER (WHERE state = 'idle') as idle
FROM pg_stat_activity
WHERE datname = 'easypost';
```

**Expected values (M3 Max):**
- Normal: 20-30 total
- Under load: 50-60 total
- Max capacity: 82 total
- Alert if > 90

---

## Nginx Proxy Commands

### Setup

```bash
# Install
brew install nginx

# Setup
bash scripts/setup-nginx-proxy.sh

# Test config
sudo nginx -t
```

### Control

```bash
# Start
sudo nginx

# Reload (after config changes)
sudo nginx -s reload

# Stop
sudo nginx -s stop

# Status
sudo nginx -s status
```

### Access Points

```bash
# Development (no proxy)
Frontend:  http://localhost:5173
Backend:   http://localhost:8000

# Production (with proxy)
Frontend:  http://localhost/
Backend:   http://localhost/api/
MCP:       http://localhost/mcp
Health:    http://localhost/health
Docs:      http://localhost/docs
```

---

## Performance Metrics

### M3 Max Pool Sizes

```python
# SQLAlchemy
pool_size = 20
max_overflow = 30
# Total: 50 connections

# asyncpg
max_size = 32
# Total: 32 connections

# Uvicorn
workers = 33
# 2x cores + 1
```

### Benchmarks

| Operation | Time | Method |
|-----------|------|--------|
| Test suite (111 tests) | 9.26s | pytest -n 16 |
| Bulk create (100) | 30-40s | EasyPost + DB |
| Batch track (50) | 2-3s | Direct pool |
| Analytics query | ~50ms | SQLAlchemy |
| Single CRUD | ~10ms | SQLAlchemy |

---

## Troubleshooting

### Too Many Connections

```sql
-- Check limit
SHOW max_connections;  -- Default: 100

-- Current usage
SELECT count(*) FROM pg_stat_activity;

-- Kill idle connections
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state = 'idle' AND state_change < now() - interval '5 minutes';
```

### Slow Queries

```sql
-- Enable logging
ALTER DATABASE easypost SET log_min_duration_statement = 1000;  -- Log queries > 1s

-- Check slow queries
SELECT
    query,
    calls,
    total_time,
    mean_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;
```

### Connection Leaks

```python
# Always use context managers
async with db_pool.acquire() as conn:
    # Do work
    pass
# Connection auto-released

# Or use Depends (auto-cleanup)
@app.get("/test")
async def test(db: AsyncSession = Depends(get_db)):
    # Session auto-closed
    pass
```

---

## Environment Variables

```bash
# .env
EASYPOST_API_KEY=EZPK_your_key

# Database
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/easypost
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=30
DATABASE_POOL_RECYCLE=3600

# Performance
WORKERS=33
PYTHONOPTIMIZE=2
```

---

## Decision Matrix

### Should I Use ORM or Direct Pool?

| Scenario | Use | Reason |
|----------|-----|--------|
| Get single shipment | ORM | Type safety, relationships |
| Create shipment | ORM | Validation, auto-commit |
| Get 100+ shipments | Direct | 3x faster bulk reads |
| Complex analytics | Direct | Raw SQL performance |
| Update many records | Direct | Bulk UPDATE faster |
| Need relationships | ORM | Automatic joins |
| Testing with mocks | ORM | Easier to mock |
| Raw performance | Direct | Lower overhead |

### Should I Add Nginx Proxy?

| Phase | Recommendation | Why |
|-------|----------------|-----|
| Local dev | No | Extra complexity, no benefit |
| Staging | Optional | Test production setup |
| Production | **Yes** | 20x faster, industry standard |
| High traffic | **Required** | Rate limiting, load balancing |

---

## Common Patterns

### Pagination

```python
@app.get("/shipments")
async def list_shipments(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Shipment)
        .offset(skip)
        .limit(limit)
        .order_by(Shipment.created_at.desc())
    )
    return result.scalars().all()
```

### Eager Loading (Avoid N+1)

```python
from sqlalchemy.orm import selectinload

result = await db.execute(
    select(Shipment).options(
        selectinload(Shipment.from_address),
        selectinload(Shipment.to_address),
        selectinload(Shipment.events)
    )
)
```

### Transactions

```python
async with db.begin():
    # Multiple operations in transaction
    shipment = Shipment(...)
    db.add(shipment)

    event = ShipmentEvent(shipment_id=shipment.id, ...)
    db.add(event)
    # Auto-commit if no exception
```

### Bulk Insert (Direct Pool)

```python
await pool.executemany(
    "INSERT INTO shipments (easypost_id, tracking_number) VALUES ($1, $2)",
    [(id1, track1), (id2, track2), ...]
)
```

---

## Health Checks

### Application Health

```bash
curl http://localhost/health
```

```json
{
  "status": "healthy",
  "database": "connected",
  "pool": {
    "size": 20,
    "active": 5
  }
}
```

### Database Health

```bash
# Quick check
psql -d easypost -c "SELECT 1"

# Detailed
psql -d easypost -c "
SELECT
    pg_database_size('easypost') / 1024 / 1024 as size_mb,
    (SELECT count(*) FROM pg_stat_activity) as connections
"
```

---

## Deployment Checklist

### Before Production

- [ ] Build frontend: `npm run build`
- [ ] Test suite passes: `pytest -n 16`
- [ ] Environment variables set
- [ ] PostgreSQL max_connections ≥ 100
- [ ] Nginx config tested: `sudo nginx -t`
- [ ] Health endpoint working
- [ ] Monitor connections: `pg_stat_activity`

### Production Start

```bash
# 1. Start backend
cd backend && source venv/bin/activate
uvicorn src.server:app --workers 33 --host 127.0.0.1 --port 8000

# 2. Start nginx
sudo nginx

# 3. Verify
curl http://localhost/health
curl http://localhost/api/health
```

---

## One-Liners

```bash
# Check connection count
psql -d easypost -tc "SELECT count(*) FROM pg_stat_activity"

# Kill all connections
psql -d easypost -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'easypost'"

# Reload nginx
sudo nginx -s reload

# Tail logs
tail -f /var/log/nginx/easypost_access.log

# Test endpoint
curl -w "\n%{time_total}s\n" http://localhost/api/health
```

---

**See full guide:** `docs/guides/PROXY_AND_DATABASE_INTEGRATION.md`

