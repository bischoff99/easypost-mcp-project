# Database & Application Monitoring Guide

**Complete monitoring guide for EasyPost MCP production deployment**

---

## Quick Start

```bash
# Monitor database connections
./scripts/monitor-database.sh

# Check application health
curl http://localhost:8000/health | jq

# View metrics
curl http://localhost:8000/metrics | jq
```

---

## Health Endpoint

### Enhanced Health Check

The `/health` endpoint now includes comprehensive monitoring:

**URL:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "system": {
    "status": "healthy",
    "cpu_percent": 15.2,
    "memory_percent": 45.8,
    "memory_available_mb": 95421.5,
    "disk_percent": 62.3,
    "disk_free_gb": 234.5
  },
  "easypost": {
    "status": "healthy",
    "latency_ms": 0
  },
  "database": {
    "status": "healthy",
    "orm_available": true,
    "asyncpg_pool": "available",
    "pool_size": 10,
    "pool_free": 8,
    "pool_used": 2,
    "pool_max": 32,
    "pool_utilization_percent": 6.25,
    "connectivity": "connected"
  },
  "timestamp": "2025-11-04T21:00:00.000Z"
}
```

**Usage:**
```bash
# Basic check
curl http://localhost:8000/health

# Pretty print
curl http://localhost:8000/health | jq

# Monitor continuously
watch -n 5 'curl -s http://localhost:8000/health | jq .database'
```

---

## Database Monitoring Script

### Quick Usage

```bash
# Run once
./scripts/monitor-database.sh

# Monitor continuously (every 30 seconds)
watch -n 30 ./scripts/monitor-database.sh

# Save to log file
./scripts/monitor-database.sh >> /var/log/easypost/db-monitor.log
```

### Output Explained

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Connection Statistics
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Max connections: 150
  Active connections: 25 / 150        ← GREEN (healthy)
  Utilization: 16.67%

  Breakdown:
    Active queries: 5                 ← Currently executing
    Idle: 20                          ← Pooled, ready to use
    Idle in transaction: 0            ← Should always be 0!
```

**Color Coding:**
- 🟢 **GREEN:** < 60% utilization (healthy)
- 🟡 **YELLOW:** 60-80% utilization (warning)
- 🔴 **RED:** > 80% utilization (critical)

**Idle in Transaction Warning:**
If you see connections stuck in "idle in transaction":
- Indicates unclosed transactions
- Can block other queries
- Should be investigated immediately

### Thresholds

```bash
# Configured in scripts/monitor-database.sh
WARNING_THRESHOLD=60   # Yellow at 60% capacity
CRITICAL_THRESHOLD=80  # Red at 80% capacity
```

**Recommended Actions:**

| Utilization | Action |
|-------------|--------|
| 0-40% | ✅ Healthy, no action |
| 40-60% | Monitor trend |
| 60-80% | ⚠️ Investigate high usage |
| 80-100% | 🚨 Reduce load or increase capacity |

---

## PostgreSQL Queries

### Connection Monitoring

**Current connection count:**
```sql
SELECT count(*) FROM pg_stat_activity WHERE datname = 'easypost_mcp';
```

**Connections by state:**
```sql
SELECT
    state,
    count(*) as connections
FROM pg_stat_activity
WHERE datname = 'easypost_mcp'
GROUP BY state
ORDER BY count(*) DESC;
```

**Expected output:**
```
  state   | connections
----------+-------------
 idle     | 20
 active   | 5
```

**Connection details:**
```sql
SELECT
    pid,
    usename,
    application_name,
    state,
    query_start,
    state_change,
    LEFT(query, 50) as query
FROM pg_stat_activity
WHERE datname = 'easypost_mcp'
ORDER BY state_change DESC;
```

### Pool Health Check

**SQLAlchemy pool usage:**
```sql
SELECT
    application_name,
    count(*) as connections,
    string_agg(DISTINCT state, ', ') as states
FROM pg_stat_activity
WHERE datname = 'easypost_mcp'
    AND application_name = 'easypost_mcp'
GROUP BY application_name;
```

**Connection age:**
```sql
SELECT
    pid,
    now() - backend_start as connection_age,
    state
FROM pg_stat_activity
WHERE datname = 'easypost_mcp'
ORDER BY backend_start ASC
LIMIT 10;
```

**Identify connection leaks:**
```sql
-- Connections open > 1 hour
SELECT
    pid,
    usename,
    state,
    now() - backend_start as age,
    now() - state_change as idle_time
FROM pg_stat_activity
WHERE datname = 'easypost_mcp'
    AND state = 'idle'
    AND now() - state_change > interval '1 hour'
ORDER BY state_change ASC;
```

### Long Running Queries

**Find slow queries (> 30 seconds):**
```sql
SELECT
    pid,
    now() - query_start as duration,
    state,
    query
FROM pg_stat_activity
WHERE datname = 'easypost_mcp'
    AND state != 'idle'
    AND now() - query_start > interval '30 seconds'
ORDER BY duration DESC;
```

**Kill stuck query:**
```sql
-- Graceful termination
SELECT pg_cancel_backend(12345);  -- Replace with actual PID

-- Force kill (if cancel doesn't work)
SELECT pg_terminate_backend(12345);
```

### Database Size Monitoring

**Total database size:**
```sql
SELECT pg_size_pretty(pg_database_size('easypost_mcp'));
```

**Table sizes:**
```sql
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS total_size,
    pg_size_pretty(pg_relation_size(schemaname||'.'||tablename)) AS table_size,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename) -
                    pg_relation_size(schemaname||'.'||tablename)) AS index_size
FROM pg_tables
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
LIMIT 10;
```

**Growth rate (compare with yesterday):**
```sql
-- Run daily and compare
SELECT
    current_database() as database,
    pg_size_pretty(pg_database_size(current_database())) as size,
    now() as measured_at;
```

---

## Application Metrics

### Metrics Endpoint

**URL:** `GET /metrics`

**Response:**
```json
{
  "uptime_seconds": 3600,
  "total_calls": 1523,
  "error_count": 12,
  "error_rate": 0.0079,
  "api_calls": {
    "create_shipment": {
      "success": 450,
      "failure": 5
    },
    "get_rates": {
      "success": 823,
      "failure": 3
    },
    "track_shipment": {
      "success": 245,
      "failure": 4
    }
  },
  "timestamp": "2025-11-04T21:00:00.000Z"
}
```

**Monitor error rate:**
```bash
# Alert if error rate > 1%
curl -s http://localhost:8000/metrics | jq '.error_rate'
```

---

## Alerting & Automation

### Watch Scripts

**Monitor connection usage:**
```bash
# Every 30 seconds
watch -n 30 './scripts/monitor-database.sh'

# Compact view
watch -n 10 'psql -U andrejs -d easypost_mcp -c "
SELECT count(*) as connections FROM pg_stat_activity WHERE datname = '\''easypost_mcp'\''"'
```

**Monitor health endpoint:**
```bash
# Every 5 seconds
watch -n 5 'curl -s http://localhost:8000/health | jq .database'
```

### Cron Jobs

**Add to crontab:**
```bash
crontab -e
```

**Suggested jobs:**
```bash
# Monitor connections every 5 minutes
*/5 * * * * /path/to/scripts/monitor-database.sh >> /var/log/easypost/db-monitor.log 2>&1

# Alert if > 80% capacity
*/10 * * * * /path/to/scripts/check-db-capacity.sh && mail -s "DB Alert" admin@example.com

# Daily database size report
0 9 * * * psql -U andrejs -d easypost_mcp -c "
SELECT pg_size_pretty(pg_database_size('easypost_mcp'))" >> /var/log/easypost/db-size.log
```

### Alert Script Example

Create `scripts/check-db-capacity.sh`:
```bash
#!/bin/bash
utilization=$(psql -U andrejs -d postgres -tAc "
SELECT round((
    (SELECT count(*) FROM pg_stat_activity WHERE datname = 'easypost_mcp')::numeric /
    (SELECT setting::int FROM pg_settings WHERE name = 'max_connections')
) * 100, 2)
")

if (( $(awk "BEGIN {print ($utilization > 80) ? 1 : 0}") )); then
    echo "ALERT: Database connection usage at ${utilization}%"
    exit 1
fi

exit 0
```

---

## Performance Monitoring

### Query Performance

**Enable slow query logging:**
```sql
-- In postgresql.conf or via ALTER SYSTEM
ALTER SYSTEM SET log_min_duration_statement = 1000;  -- Log queries > 1s
SELECT pg_reload_conf();
```

**View slow query stats:**
```sql
-- Requires pg_stat_statements extension
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

SELECT
    queryid,
    LEFT(query, 50) as query,
    calls,
    total_exec_time,
    mean_exec_time,
    max_exec_time
FROM pg_stat_statements
WHERE dbid = (SELECT oid FROM pg_database WHERE datname = 'easypost_mcp')
ORDER BY mean_exec_time DESC
LIMIT 10;
```

### Index Effectiveness

**Unused indexes (wasted space):**
```sql
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan as scans,
    pg_size_pretty(pg_relation_size(indexrelid)) as size
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
    AND idx_scan = 0
    AND pg_relation_size(indexrelid) > 1024 * 1024  -- > 1MB
ORDER BY pg_relation_size(indexrelid) DESC;
```

**Index hit ratio (should be > 99%):**
```sql
SELECT
    round(
        100.0 * sum(idx_blks_hit) / NULLIF(sum(idx_blks_hit + idx_blks_read), 0),
        2
    ) as index_hit_ratio_percent
FROM pg_statio_user_indexes;
```

---

## Grafana Dashboards (Optional)

### Setup Prometheus + Grafana

**1. Install postgres_exporter:**
```bash
brew install postgres_exporter

# Configure
export DATA_SOURCE_NAME="postgresql://andrejs@localhost/easypost_mcp?sslmode=disable"
postgres_exporter
```

**2. Key Metrics to Track:**

```promql
# Connection pool usage
pg_stat_activity_count{datname="easypost_mcp"}

# Connection states
pg_stat_activity_count{datname="easypost_mcp",state="active"}
pg_stat_activity_count{datname="easypost_mcp",state="idle"}

# Database size
pg_database_size_bytes{datname="easypost_mcp"}

# Query performance
rate(pg_stat_statements_total_time_seconds[5m])
```

**3. Alert Rules:**

```yaml
# alerts.yml
groups:
  - name: easypost_database
    rules:
      - alert: HighConnectionUsage
        expr: pg_stat_activity_count{datname="easypost_mcp"} > 120
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Database connection usage high"

      - alert: IdleInTransaction
        expr: pg_stat_activity_count{datname="easypost_mcp",state="idle in transaction"} > 0
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Connections stuck in idle transaction"
```

---

## Troubleshooting

### Connection Exhaustion

**Symptoms:**
```
ERROR: remaining connection slots are reserved for non-replication superuser connections
```

**Diagnosis:**
```sql
SELECT count(*) FROM pg_stat_activity WHERE datname = 'easypost_mcp';
-- If near max_connections (150), you have exhaustion
```

**Quick fix:**
```sql
-- Kill idle connections
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname = 'easypost_mcp'
    AND state = 'idle'
    AND state_change < now() - interval '10 minutes';
```

**Long-term fix:**
```bash
# Option 1: Reduce pool sizes
# .env
DATABASE_POOL_SIZE=15
DATABASE_MAX_OVERFLOW=20

# Option 2: Increase PostgreSQL limit
psql -U andrejs -d postgres
ALTER SYSTEM SET max_connections = 200;
SELECT pg_reload_conf();
-- Then restart: brew services restart postgresql@17
```

### Pool Connection Leaks

**Symptoms:**
- Pool exhausted but low PostgreSQL connections
- Application hangs on database calls

**Diagnosis:**
```python
# In application health check
{
  "database": {
    "pool_size": 32,
    "pool_free": 0,     ← No free connections!
    "pool_used": 32     ← All in use
  }
}
```

**Fix:**
```bash
# Restart application to reset pools
# or
# Fix code to ensure connections are released (use context managers)
```

### Long Running Queries

**Symptoms:**
- Slow application response
- High CPU on PostgreSQL

**Diagnosis:**
```sql
SELECT
    pid,
    now() - query_start as duration,
    state,
    query
FROM pg_stat_activity
WHERE datname = 'easypost_mcp'
    AND now() - query_start > interval '30 seconds'
ORDER BY duration DESC;
```

**Fix:**
```sql
-- Cancel query (graceful)
SELECT pg_cancel_backend(PID);

-- Terminate (force)
SELECT pg_terminate_backend(PID);
```

---

## Production Monitoring Setup

### Recommended Stack

```
Application → Health Endpoint
         ↓
   Prometheus (metrics collection)
         ↓
    Grafana (visualization)
         ↓
   AlertManager (notifications)
```

### Minimal Setup (No External Tools)

**1. Create monitoring script:**
```bash
# scripts/health-check.sh
#!/bin/bash

# Check application
if ! curl -sf http://localhost:8000/health > /dev/null; then
    echo "Application unhealthy"
    exit 1
fi

# Check database
connections=$(psql -U andrejs -d postgres -tAc "
SELECT count(*) FROM pg_stat_activity WHERE datname = 'easypost_mcp'
")

if [ "$connections" -gt 120 ]; then
    echo "Too many connections: $connections"
    exit 1
fi

echo "All systems healthy"
exit 0
```

**2. Run via cron:**
```bash
*/5 * * * * /path/to/scripts/health-check.sh || mail -s "EasyPost Alert" admin@example.com
```

---

## M3 Max Specific Monitoring

### CPU & Memory

**Expected usage (33 workers):**
```
CPU:
├─ Normal load: 20-40% (3-6 cores)
├─ Peak load: 60-80% (10-13 cores)
└─ Max capacity: 95% (15 cores, 1 reserved)

Memory:
├─ Base: ~2 GB (Python + pools)
├─ Normal: ~4-6 GB (with connections)
├─ Peak: ~8-10 GB (full load)
└─ Available: 128 GB total
```

**Monitor:**
```bash
# CPU per worker
ps aux | grep uvicorn | awk '{sum+=$3} END {print "CPU:", sum"%"}'

# Memory usage
ps aux | grep uvicorn | awk '{sum+=$6} END {print "Memory:", sum/1024"MB"}'
```

### Worker Process Monitoring

**Check worker health:**
```bash
# Count workers
pgrep -f "uvicorn" | wc -l
# Should be: 33 (configured workers)

# Worker CPU usage
ps aux | grep "uvicorn worker" | awk '{print $2, $3"%", $11}'
```

**Restart workers if needed:**
```bash
# Graceful reload
kill -HUP $(pgrep -f "uvicorn.*master")

# Full restart
pkill -f uvicorn
cd backend && uvicorn src.server:app --workers 33
```

---

## Monitoring Checklist

### Daily
- [ ] Run `./scripts/monitor-database.sh`
- [ ] Check `curl http://localhost:8000/health`
- [ ] Review error rate in `/metrics`
- [ ] Check application logs for warnings

### Weekly
- [ ] Review slow query log
- [ ] Check database growth rate
- [ ] Verify index usage
- [ ] Review connection patterns

### Monthly
- [ ] Analyze performance trends
- [ ] Review and optimize slow queries
- [ ] Check for unused indexes
- [ ] Update pool sizes if needed

---

## Example Monitoring Workflow

```bash
# 1. Quick health check
curl http://localhost:8000/health | jq '.database'

# 2. If issues detected, run full monitoring
./scripts/monitor-database.sh

# 3. Check specific connections
psql -U andrejs -d easypost_mcp -c "
SELECT * FROM pg_stat_activity WHERE datname = 'easypost_mcp'"

# 4. View application metrics
curl http://localhost:8000/metrics | jq

# 5. Check logs
tail -f /path/to/easypost/logs/app.log
```

---

## Commands Reference

```bash
# Database monitoring
./scripts/monitor-database.sh              # Full report
watch -n 30 ./scripts/monitor-database.sh  # Continuous

# Application health
curl http://localhost:8000/health | jq
curl http://localhost:8000/metrics | jq

# PostgreSQL queries
psql -U andrejs -d easypost_mcp -c "SELECT count(*) FROM pg_stat_activity"
psql -U andrejs -d easypost_mcp -c "SELECT * FROM pg_stat_activity WHERE state = 'active'"

# Kill connections
psql -U andrejs -d postgres -c "SELECT pg_terminate_backend(PID)"

# Restart services
brew services restart postgresql@17
pkill -f uvicorn && uvicorn src.server:app --workers 33
```

---

**See also:**
- `DATABASE_SETUP_REVIEW.md` - Complete database analysis
- `docs/guides/QUICK_REFERENCE.md` - Code patterns
- `scripts/monitor-database.sh` - Automated monitoring

