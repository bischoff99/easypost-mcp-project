#!/bin/bash
# Database Connection Monitoring Script for EasyPost MCP
# Monitors PostgreSQL connection usage and pool health

set -euo pipefail

# Configuration
DB_NAME="${DATABASE_NAME:-easypost_mcp}"
DB_USER="${DATABASE_USER:-andrejs}"
DB_HOST="${DATABASE_HOST:-localhost}"
WARNING_THRESHOLD=60  # Warning at 60% capacity
CRITICAL_THRESHOLD=80  # Critical at 80% capacity

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${BLUE}  $1${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
}

print_metric() {
    local label="$1"
    local value="$2"
    local threshold="${3:-}"

    if [ -n "$threshold" ]; then
        # Use awk for comparison (more portable than bc)
        local is_critical=$(awk "BEGIN {print ($value > $CRITICAL_THRESHOLD) ? 1 : 0}")
        local is_warning=$(awk "BEGIN {print ($value > $WARNING_THRESHOLD) ? 1 : 0}")

        if [ "$is_critical" -eq 1 ]; then
            echo -e "${RED}  $label: $value${NC}"
        elif [ "$is_warning" -eq 1 ]; then
            echo -e "${YELLOW}  $label: $value${NC}"
        else
            echo -e "${GREEN}  $label: $value${NC}"
        fi
    else
        echo "  $label: $value"
    fi
}

get_connection_stats() {
    psql -U "$DB_USER" -d "$DB_NAME" -t -A -F',' -c "
    SELECT
        (SELECT setting::int FROM pg_settings WHERE name = 'max_connections'),
        (SELECT count(*) FROM pg_stat_activity WHERE datname = '$DB_NAME'),
        (SELECT count(*) FROM pg_stat_activity WHERE datname = '$DB_NAME' AND state = 'active'),
        (SELECT count(*) FROM pg_stat_activity WHERE datname = '$DB_NAME' AND state = 'idle'),
        (SELECT count(*) FROM pg_stat_activity WHERE datname = '$DB_NAME' AND state = 'idle in transaction')
    " 2>/dev/null
}

check_long_running_queries() {
    psql -U "$DB_USER" -d "$DB_NAME" -c "
    SELECT
        pid,
        now() - query_start as duration,
        state,
        LEFT(query, 50) as query
    FROM pg_stat_activity
    WHERE datname = '$DB_NAME'
        AND state != 'idle'
        AND now() - query_start > interval '30 seconds'
    ORDER BY duration DESC
    LIMIT 5
    " 2>/dev/null
}

check_database_size() {
    psql -U "$DB_USER" -d "$DB_NAME" -t -c "
    SELECT pg_size_pretty(pg_database_size('$DB_NAME'))
    " 2>/dev/null
}

check_table_sizes() {
    psql -U "$DB_USER" -d "$DB_NAME" -c "
    SELECT
        schemaname,
        tablename,
        pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
    FROM pg_tables
    WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
    ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
    LIMIT 10
    " 2>/dev/null
}

check_index_usage() {
    psql -U "$DB_USER" -d "$DB_NAME" -c "
    SELECT
        schemaname,
        tablename,
        indexname,
        idx_scan as index_scans,
        pg_size_pretty(pg_relation_size(indexrelid)) as index_size
    FROM pg_stat_user_indexes
    WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
        AND idx_scan = 0
        AND pg_relation_size(indexrelid) > 1024 * 1024  -- Larger than 1MB
    ORDER BY pg_relation_size(indexrelid) DESC
    LIMIT 5
    " 2>/dev/null
}

# Main monitoring
print_header "Database Connection Monitor - EasyPost MCP"

echo "Database: $DB_NAME"
echo "User: $DB_USER"
echo "Host: $DB_HOST"
echo "Timestamp: $(date '+%Y-%m-%d %H:%M:%S')"

# Get connection statistics
print_header "Connection Statistics"

if ! stats=$(get_connection_stats); then
    echo -e "${RED}Error: Could not connect to database${NC}"
    echo "Please check:"
    echo "  1. PostgreSQL is running: brew services list | grep postgres"
    echo "  2. Database exists: psql -l | grep $DB_NAME"
    echo "  3. User has access: psql -U $DB_USER -d $DB_NAME -c 'SELECT 1'"
    exit 1
fi

# Parse stats (comma-separated)
max_connections=$(echo "$stats" | cut -d',' -f1)
active_connections=$(echo "$stats" | cut -d',' -f2)
active_queries=$(echo "$stats" | cut -d',' -f3)
idle_connections=$(echo "$stats" | cut -d',' -f4)
idle_in_transaction=$(echo "$stats" | cut -d',' -f5)

# Calculate utilization (using awk for better portability)
utilization=$(awk "BEGIN {printf \"%.2f\", ($active_connections / $max_connections) * 100}")

echo "  Max connections: $max_connections"
print_metric "Active connections" "$active_connections / $max_connections" "$utilization"
echo "  Utilization: ${utilization}%"
echo ""
echo "  Breakdown:"
echo "    Active queries: $active_queries"
echo "    Idle: $idle_connections"

if [ "$idle_in_transaction" -gt 0 ]; then
    echo -e "    ${YELLOW}Idle in transaction: $idle_in_transaction (investigate!)${NC}"
else
    echo "    Idle in transaction: $idle_in_transaction"
fi

# Pool Analysis
print_header "Connection Pool Analysis"

echo "  EasyPost MCP Pools:"
echo "    • SQLAlchemy ORM: 20 base + 30 overflow = 50 max"
echo "    • asyncpg Direct: 10 min + 32 max"
echo "    • Total Capacity: 82 connections"
echo ""

available=$((max_connections - active_connections))
echo "  Available connections: $available"

if [ "$available" -lt 20 ]; then
    echo -e "  ${RED}⚠️  WARNING: Low available connections!${NC}"
elif [ "$available" -lt 50 ]; then
    echo -e "  ${YELLOW}⚠️  Approaching capacity${NC}"
else
    echo -e "  ${GREEN}✅ Healthy capacity${NC}"
fi

# Long Running Queries
print_header "Long Running Queries (> 30s)"

if ! long_queries=$(check_long_running_queries); then
    echo "  No long-running queries detected ✅"
else
    if [ -z "$(echo "$long_queries" | tail -n +3)" ]; then
        echo "  No long-running queries detected ✅"
    else
        echo "$long_queries"
        echo ""
        echo -e "  ${YELLOW}Tip: Kill stuck query with: SELECT pg_terminate_backend(pid);${NC}"
    fi
fi

# Database Size
print_header "Database Size"

db_size=$(check_database_size | xargs)
echo "  Total database size: $db_size"

# Top Tables by Size
print_header "Top 10 Tables by Size"
check_table_sizes

# Unused Indexes
print_header "Unused Indexes (> 1MB, never scanned)"
unused_indexes=$(check_index_usage | tail -n +3)

if [ -z "$unused_indexes" ]; then
    echo "  All indexes are being used ✅"
else
    check_index_usage
    echo ""
    echo -e "  ${YELLOW}Tip: Consider dropping unused indexes to improve write performance${NC}"
fi

# Health Summary
print_header "Health Summary"

issues=0

# Use awk for float comparison
is_critical=$(awk "BEGIN {print ($utilization > $CRITICAL_THRESHOLD) ? 1 : 0}")
is_warning=$(awk "BEGIN {print ($utilization > $WARNING_THRESHOLD) ? 1 : 0}")

if [ "$is_critical" -eq 1 ]; then
    echo -e "${RED}  ❌ CRITICAL: Connection usage at ${utilization}%${NC}"
    issues=$((issues + 1))
elif [ "$is_warning" -eq 1 ]; then
    echo -e "${YELLOW}  ⚠️  WARNING: Connection usage at ${utilization}%${NC}"
    issues=$((issues + 1))
else
    echo -e "${GREEN}  ✅ Connection usage healthy (${utilization}%)${NC}"
fi

if [ "$idle_in_transaction" -gt 0 ]; then
    echo -e "${YELLOW}  ⚠️  WARNING: $idle_in_transaction connections idle in transaction${NC}"
    issues=$((issues + 1))
fi

if [ "$issues" -eq 0 ]; then
    echo -e "${GREEN}  ✅ All systems healthy${NC}"
else
    echo ""
    echo -e "${YELLOW}  Issues detected: $issues${NC}"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Recommendations
if [ "$issues" -gt 0 ]; then
    echo "💡 Recommendations:"
    echo ""

    if [ "$is_warning" -eq 1 ] || [ "$is_critical" -eq 1 ]; then
        echo "  • Consider reducing pool sizes:"
        echo "    DATABASE_POOL_SIZE=15"
        echo "    DATABASE_MAX_OVERFLOW=20"
        echo ""
        echo "  • Or increase PostgreSQL max_connections:"
        echo "    ALTER SYSTEM SET max_connections = 200;"
        echo ""
    fi

    if [ "$idle_in_transaction" -gt 0 ]; then
        echo "  • Investigate idle in transaction connections:"
        echo "    SELECT * FROM pg_stat_activity WHERE state = 'idle in transaction';"
        echo ""
        echo "  • Kill stuck transactions:"
        echo "    SELECT pg_terminate_backend(pid) FROM pg_stat_activity"
        echo "    WHERE state = 'idle in transaction' AND state_change < now() - interval '5 minutes';"
        echo ""
    fi
fi

exit $issues

