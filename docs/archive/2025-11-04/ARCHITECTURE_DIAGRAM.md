# EasyPost MCP Architecture Diagram

**Visual guide to reverse proxy + PostgreSQL integration**

---

## Current Development Setup

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│   USER BROWSER                                      │
│                                                     │
└──────┬─────────────────────────────┬────────────────┘
       │                             │
       │                             │
   ┌───▼────────┐              ┌─────▼──────────┐
   │ Frontend   │              │ Backend        │
   │ :5173      │              │ :8000          │
   │            │              │                │
   │ Vite Dev   │              │ FastAPI        │
   │ Hot reload │              │ Uvicorn        │
   └────────────┘              └────┬───────────┘
                                    │
                         ┌──────────┼──────────┐
                         │                     │
                    ┌────▼─────┐         ┌─────▼────────┐
                    │ EasyPost │         │ PostgreSQL   │
                    │ API      │         │              │
                    │          │         │ 2 Pools:     │
                    │ Rate:    │         │ • ORM: 50    │
                    │ 16/s     │         │ • Direct: 32 │
                    └──────────┘         └──────────────┘

Issues:
❌ CORS required (different origins)
❌ Node serves static (slow)
❌ No asset caching
```

---

## Production Setup with Nginx Proxy

```
┌──────────────────────────────────────────────────────────┐
│                                                          │
│   USER BROWSER                                           │
│                                                          │
└──────────────────────┬───────────────────────────────────┘
                       │
                       │ http://localhost
                       │
                ┌──────▼─────────┐
                │                │
                │  Nginx :80     │  ← Single Entry Point
                │                │
                │  • Static      │  ← 20x faster
                │  • Rate limit  │  ← Before Python
                │  • Caching     │  ← Browser cache
                │  • SSL         │  ← HTTPS ready
                │                │
                └───┬────────┬───┘
                    │        │
        ┌───────────┘        └───────────────┐
        │                                    │
        │ /                           /api/*, /mcp
        │                                    │
   ┌────▼─────────┐              ┌──────────▼────────────┐
   │              │              │                       │
   │  Frontend    │              │  Backend              │
   │  (Static)    │              │  :8000                │
   │              │              │                       │
   │  nginx       │              │  FastAPI              │
   │  serves      │              │  33 workers           │
   │  dist/       │              │  (M3 Max: 2×16+1)     │
   │              │              │                       │
   │  Cache:      │              └───┬──────────┬────────┘
   │  • 1 year    │                  │          │
   │  • gzip      │                  │          │
   └──────────────┘                  │          │
                              ┌──────▼──┐  ┌────▼─────────┐
                              │EasyPost │  │ PostgreSQL   │
                              │API      │  │              │
                              │         │  │ Pools:       │
                              │Rate:    │  │              │
                              │16/s     │  │ ┌──────────┐ │
                              │(sema)   │  │ │SQLAlchemy│ │
                              └─────────┘  │ │ORM Pool  │ │
                                           │ │          │ │
                                           │ │Size: 20  │ │
                                           │ │Overflow:30│ │
                                           │ │Total: 50 │ │
                                           │ └──────────┘ │
                                           │              │
                                           │ ┌──────────┐ │
                                           │ │asyncpg   │ │
                                           │ │Direct    │ │
                                           │ │Pool      │ │
                                           │ │          │ │
                                           │ │Size: 32  │ │
                                           │ │(2×cores) │ │
                                           │ └──────────┘ │
                                           │              │
                                           │ Max: 100     │
                                           │ Used: 82     │
                                           └──────────────┘

Benefits:
✅ Single origin (no CORS)
✅ Static caching (instant loads)
✅ Rate limiting at edge
✅ Production-ready
```

---

## Database Connection Pools (Detailed)

```
┌────────────────────────────────────────────────────────┐
│  FastAPI Application (33 Workers)                     │
└─────┬──────────────────────────────────┬───────────────┘
      │                                  │
      │                                  │
      │ Depends(get_db)                  │ app.state.db_pool
      │                                  │
┌─────▼──────────────────┐      ┌────────▼────────────────┐
│                        │      │                         │
│  SQLAlchemy ORM Pool   │      │  asyncpg Direct Pool    │
│                        │      │                         │
│  Configuration:        │      │  Configuration:         │
│  • pool_size: 20       │      │  • min_size: 10         │
│  • max_overflow: 30    │      │  • max_size: 32         │
│  • pool_recycle: 3600s │      │  • timeout: 60s         │
│  • pool_pre_ping: True │      │  • statement_cache: 500 │
│                        │      │                         │
│  Total: 50 connections │      │  Total: 32 connections  │
│                        │      │                         │
│  Use for:              │      │  Use for:               │
│  ✓ CRUD operations     │      │  ✓ Bulk operations      │
│  ✓ Relationships       │      │  ✓ Analytics queries    │
│  ✓ Type safety         │      │  ✓ Raw SQL performance  │
│  ✓ Migrations          │      │  ✓ Parallel processing  │
│                        │      │                         │
└────────┬───────────────┘      └─────────┬───────────────┘
         │                                │
         └────────────┬───────────────────┘
                      │
              ┌───────▼────────┐
              │                │
              │  PostgreSQL    │
              │                │
              │  max: 100      │
              │  used: 82      │
              │  free: 18      │
              │                │
              └────────────────┘
```

---

## Request Flow Examples

### Example 1: Get Single Shipment (ORM)

```
User Request
    ↓
GET /api/shipments/123
    ↓
Nginx :80
    ↓ proxy_pass
FastAPI Worker #5
    ↓ Depends(get_db)
SQLAlchemy Pool
    ↓ acquire connection #12
PostgreSQL
    ↓ SELECT with joins
┌───────────────────────────┐
│ SELECT s.*, a1.*, a2.*    │
│ FROM shipments s          │
│ JOIN addresses a1 ...     │
│ JOIN addresses a2 ...     │
└───────────────────────────┘
    ↓
Connection released to pool
    ↓
Response (JSON) ← FastAPI
    ↓ proxy_pass
Nginx (cache headers)
    ↓
User Browser
```

**Time:** ~10-20ms  
**Pool:** SQLAlchemy ORM  
**Connection:** Reused from pool

### Example 2: Bulk Shipment Creation (Both Pools)

```
User Request
    ↓
POST /api/shipments/bulk-create
Body: [100 shipments]
    ↓
Nginx :80
    ↓ proxy_pass
FastAPI Worker #3
    ↓
Rate Limiter (16 concurrent)
    ↓
asyncio.gather (16 parallel tasks)
    ├─────┬─────┬─────┬─────┐
    ▼     ▼     ▼     ▼     ▼
 Task1 Task2 Task3 ... Task16
    │     │     │         │
    ↓     ↓     ↓         ↓
EasyPost API (16 concurrent)
    │     │     │         │
    ↓     ↓     ↓         ↓
 Label Label Label ... Label
    │     │     │         │
    ↓     ↓     ↓         ↓
asyncpg Direct Pool
    │     │     │         │
    ├─────┴─────┴─────────┤
    │ 16 connections used  │
    ↓                      ↓
INSERT INTO shipments ...
    ↓
PostgreSQL (bulk insert)
    ↓
Connections released
    ↓
Response (JSON)
    ↓
User Browser
```

**Time:** 30-40s for 100 shipments  
**Pool:** asyncpg (direct)  
**Concurrency:** 16 parallel (rate limiter)  
**EasyPost:** 16 concurrent API calls  
**Database:** 16 connections active

### Example 3: Analytics Query (Direct Pool)

```
User Request
    ↓
GET /api/analytics/2025-11-04
    ↓
Nginx :80
    ↓ proxy_pass
FastAPI Worker #8
    ↓
app.state.db_pool.fetch()
    ↓
asyncpg Direct Pool
    ↓ acquire connection #7
PostgreSQL
    ↓ Complex aggregation
┌───────────────────────────────┐
│ SELECT                        │
│   date,                       │
│   COUNT(*) as total,          │
│   SUM(cost) as revenue,       │
│   AVG(cost) as avg_cost       │
│ FROM shipments                │
│ WHERE date = $1               │
│ GROUP BY date                 │
└───────────────────────────────┘
    ↓
Connection released
    ↓
Response (JSON)
    ↓ proxy_pass
Nginx
    ↓
User Browser
```

**Time:** ~50ms  
**Pool:** asyncpg (direct)  
**Why:** Complex aggregation faster with raw SQL

---

## Nginx Routing Logic

```
                 ┌─────────────────┐
                 │  Nginx :80      │
                 └────────┬────────┘
                          │
              ┌───────────┴────────────┐
              │ Check request path     │
              └───────────┬────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        │                 │                 │
   ┌────▼────┐       ┌────▼────┐      ┌────▼────┐
   │   /     │       │ /api/*  │      │  /mcp   │
   └────┬────┘       └────┬────┘      └────┬────┘
        │                 │                 │
   ┌────▼─────────┐  ┌────▼──────┐    ┌────▼──────┐
   │ Serve static │  │ Strip /api│    │ No strip  │
   │ from dist/   │  │ Proxy to  │    │ Proxy to  │
   │              │  │ :8000     │    │ :8000/mcp │
   │ • Cache 1yr  │  │           │    │           │
   │ • gzip on    │  │ • Rate    │    │ • Timeout │
   │ • No log     │  │   limit   │    │   120s    │
   └──────────────┘  └───────────┘    └───────────┘
```

---

## M3 Max Resource Allocation

```
┌─────────────────────────────────────────────────┐
│  M3 Max (16 cores, 128 GB RAM)                 │
└─────────────────────────────────────────────────┘
            │
   ┌────────┼────────┐
   │                 │
┌──▼──────────┐  ┌───▼─────────┐
│ CPU Cores   │  │ Memory      │
│             │  │             │
│ 12 Perform. │  │ 128 GB      │
│  4 Effic.   │  │             │
│             │  │ Usage:      │
│ Total: 16   │  │ • Nginx: 1GB│
└──┬──────────┘  │ • Python:8GB│
   │             │ • Postgres:│
   │             │   20GB      │
   │             └─────────────┘
   │
   ├─────────────┐
   │             │
┌──▼──────────┐  │
│ Nginx       │  │
│ 1-2 cores   │  │
└─────────────┘  │
                 │
┌────────────────▼───────────────┐
│ Uvicorn Workers                │
│                                │
│ Count: 33 (2 × cores + 1)      │
│ CPU: ~14 cores                 │
│ Each: ~250 MB                  │
└────────┬───────────────────────┘
         │
┌────────▼───────────────────────┐
│ Database Connections           │
│                                │
│ ORM Pool: 50 connections       │
│ Direct Pool: 32 connections    │
│ Total: 82 active connections   │
└────────────────────────────────┘
```

---

## Performance Comparison

### Without Proxy (Development)

```
┌────────────┐
│ Request    │
└─────┬──────┘
      │
      ├──────────────────┐
      │                  │
┌─────▼──────┐    ┌──────▼──────┐
│ Vite :5173 │    │ Uvicorn     │
│ Node.js    │    │ :8000       │
│            │    │             │
│ vendor.js  │    │ CORS check  │
│ 341 KB     │    │ (2ms)       │
│ Serve: 10ms│    │             │
└────────────┘    └──────┬──────┘
                         │
                  ┌──────▼──────┐
                  │ PostgreSQL  │
                  └─────────────┘

Total time:
• Static file: 10ms
• API call: 2ms (CORS) + 10ms (query) = 12ms
```

### With Proxy (Production)

```
┌────────────┐
│ Request    │
└─────┬──────┘
      │
┌─────▼──────┐
│ Nginx :80  │
│            │
├────────────┤
│ /assets/*  │ ← Static
│ Cached     │
│ 0.5ms      │
├────────────┤
│ /api/*     │ ← API
│ Proxy      │
└─────┬──────┘
      │
┌─────▼──────┐
│ Uvicorn    │
│ :8000      │
│            │
│ No CORS    │
└─────┬──────┘
      │
┌─────▼──────┐
│ PostgreSQL │
└────────────┘

Total time:
• Static file: 0.5ms (20x faster)
• API call: 10ms (no CORS overhead)
• Cached static: 0ms (304 Not Modified)
```

---

## Connection Pool Lifecycle

```
┌─────────────────────────────────────────────────┐
│  Application Startup (lifespan)                │
└─────────────────────────────────────────────────┘
                   │
      ┌────────────┼────────────┐
      │                         │
┌─────▼──────────┐      ┌───────▼───────┐
│ Create ORM     │      │ Create asyncpg│
│ Engine         │      │ Pool          │
│                │      │               │
│ await          │      │ await         │
│ engine.begin() │      │ create_pool() │
└────────────────┘      └───────────────┘
                   │
        ┌──────────┴──────────┐
        │ Pools Ready         │
        │ Connections: 0      │
        └──────────┬──────────┘
                   │
        ┌──────────▼──────────┐
        │ Handle Requests     │
        │                     │
        │ Acquire on demand   │
        │ Release after use   │
        │ Pool grows to size  │
        └──────────┬──────────┘
                   │
        ┌──────────▼──────────┐
        │ Steady State        │
        │                     │
        │ ORM: 20 idle        │
        │ Direct: 10 idle     │
        │ Total: 30 ready     │
        └──────────┬──────────┘
                   │
        ┌──────────▼──────────┐
        │ Under Load          │
        │                     │
        │ ORM: 50 active      │
        │ Direct: 32 active   │
        │ Total: 82 busy      │
        └──────────┬──────────┘
                   │
        ┌──────────▼──────────┐
        │ Application         │
        │ Shutdown            │
        │                     │
        │ await pool.close()  │
        │ Connections drained │
        └─────────────────────┘
```

---

## Summary

**Current Setup (Development):**
- ✅ Working perfectly for dev
- ❌ CORS required
- ❌ No caching

**Production Setup (Add Nginx):**
- ✅ 20x faster static delivery
- ✅ Single URL (no CORS)
- ✅ Edge rate limiting
- ✅ Production-ready

**PostgreSQL (Already Optimal):**
- ✅ Dual pools for different use cases
- ✅ M3 Max optimized (82 connections)
- ✅ Industry best practices

**Next Step:** Run `bash scripts/setup-nginx-proxy.sh` before production
