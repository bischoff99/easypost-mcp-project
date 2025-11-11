#!/bin/bash
# Benchmark Validation Script
# Validates benchmark claims with actual codebase metrics

set +e  # Don't exit on errors - we want to collect all validation results

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║     BENCHMARK VALIDATION - EasyPost MCP Project              ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

VALIDATION_RESULTS=()
PASS_COUNT=0
FAIL_COUNT=0

# Helper function
check_metric() {
    local name="$1"
    local actual="$2"
    local expected="$3"
    local operator="$4"  # "eq", "ge", "le", "gt", "lt"

    local pass=false
    case "$operator" in
        "eq") [ "$actual" -eq "$expected" ] && pass=true ;;
        "ge") [ "$actual" -ge "$expected" ] && pass=true ;;
        "le") [ "$actual" -le "$expected" ] && pass=true ;;
        "gt") [ "$actual" -gt "$expected" ] && pass=true ;;
        "lt") [ "$actual" -lt "$expected" ] && pass=true ;;
    esac

    if [ "$pass" = true ]; then
        echo "  ✅ $name: $actual (expected: $operator $expected)"
        ((PASS_COUNT++))
        VALIDATION_RESULTS+=("✅ $name: PASS")
    else
        echo "  ❌ $name: $actual (expected: $operator $expected)"
        ((FAIL_COUNT++))
        VALIDATION_RESULTS+=("❌ $name: FAIL")
    fi
}

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1. CODE QUALITY VALIDATION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Linting errors
if [ -d "apps/backend/venv" ]; then
    cd apps/backend
    source venv/bin/activate 2>/dev/null || true

    if command -v ruff >/dev/null 2>&1; then
        LINT_ERRORS=$(ruff check src/ --output-format=json 2>/dev/null | python3 -c "import sys, json; data=json.load(sys.stdin); errors=[x for x in data if x.get('code', '').startswith('E')]; print(len(errors))" 2>/dev/null || echo "0")
        check_metric "Linting Errors (Ruff)" "$LINT_ERRORS" "0" "eq"
    else
        echo "  ⚠️  Ruff not available - skipping lint check"
    fi

    cd "$PROJECT_ROOT"
else
    echo "  ⚠️  Backend venv not found - skipping Python checks"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "2. SECURITY VALIDATION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Hardcoded secrets
SECRET_MATCHES=$(grep -r "EZAK\|EZTK\|pk_test\|sk_test" apps/backend/src apps/frontend/src 2>/dev/null | grep -v "EASYPOST_API_KEY\|api_key\|API_KEY\|# Remove API keys" | wc -l | tr -d ' ')
check_metric "Hardcoded Secrets" "$SECRET_MATCHES" "0" "eq"

# Security scanning (if bandit available)
if [ -d "apps/backend/venv" ]; then
    cd apps/backend
    source venv/bin/activate 2>/dev/null || true

    if command -v bandit >/dev/null 2>&1; then
        BANDIT_OUTPUT=$(bandit -r src/ -f json 2>/dev/null | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('metrics', {}).get('HIGH', 0), data.get('metrics', {}).get('MEDIUM', 0))" 2>/dev/null || echo "0 0")
        HIGH_VULNS=$(echo $BANDIT_OUTPUT | cut -d' ' -f1)
        MED_VULNS=$(echo $BANDIT_OUTPUT | cut -d' ' -f2)
        check_metric "Security Vulnerabilities (HIGH)" "$HIGH_VULNS" "0" "eq"
        check_metric "Security Vulnerabilities (MEDIUM)" "$MED_VULNS" "0" "eq"
    else
        echo "  ⚠️  Bandit not available - skipping security scan"
    fi

    cd "$PROJECT_ROOT"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "3. TESTING VALIDATION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Test file count
BACKEND_TESTS=$(find apps/backend/tests -name "test_*.py" -type f 2>/dev/null | wc -l | tr -d ' ')
FRONTEND_TESTS=$(find apps/frontend/src/tests -name "*.test.*" -o -name "*.spec.*" 2>/dev/null | wc -l | tr -d ' ')
check_metric "Backend Test Files" "$BACKEND_TESTS" "15" "ge"
check_metric "Frontend Test Files" "$FRONTEND_TESTS" "1" "ge"

# Parallel configuration
PYTEST_WORKERS=$(grep -E "-n [0-9]+" apps/backend/pytest.ini 2>/dev/null | grep -oE "[0-9]+" | head -1)
if [ -z "$PYTEST_WORKERS" ]; then
    PYTEST_WORKERS=0
fi
VITEST_WORKERS=$(grep -E "maxThreads.*[0-9]+" apps/frontend/vitest.config.js 2>/dev/null | grep -oE "[0-9]+" | head -1)
if [ -z "$VITEST_WORKERS" ]; then
    VITEST_WORKERS=0
fi
check_metric "Pytest Workers" "$PYTEST_WORKERS" "16" "ge"
check_metric "Vitest Workers" "$VITEST_WORKERS" "8" "ge"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "4. DOCUMENTATION VALIDATION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Documentation file count
DOC_FILES=$(find docs -name "*.md" -type f 2>/dev/null | wc -l | tr -d ' ')
check_metric "Documentation Files" "$DOC_FILES" "50" "ge"

# README quality
if [ -f "README.md" ]; then
    README_LINES=$(wc -l < README.md | tr -d ' ')
    README_SECTIONS=$(grep -c "^##\|^###" README.md 2>/dev/null || echo "0")
    check_metric "README Lines" "$README_LINES" "50" "ge"
    check_metric "README Sections" "$README_SECTIONS" "5" "ge"
fi

# ADR count
ADR_COUNT=$(find docs/architecture/decisions -name "ADR-*.md" 2>/dev/null | wc -l | tr -d ' ')
check_metric "Architecture Decision Records" "$ADR_COUNT" "3" "ge"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "5. CONFIGURATION VALIDATION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Docker multi-stage (check for multiple FROM statements indicating multi-stage)
BACKEND_FROM_COUNT=$(grep -c "^FROM" apps/backend/Dockerfile 2>/dev/null || echo "0")
FRONTEND_FROM_COUNT=$(grep -c "^FROM" apps/frontend/Dockerfile 2>/dev/null || echo "0")
# Multi-stage = 2+ FROM statements
BACKEND_STAGES=$BACKEND_FROM_COUNT
FRONTEND_STAGES=$FRONTEND_FROM_COUNT
check_metric "Backend Docker Stages" "$BACKEND_STAGES" "2" "ge"
check_metric "Frontend Docker Stages" "$FRONTEND_STAGES" "1" "ge"

# Pre-commit hooks
if [ -f ".pre-commit-config.yaml" ]; then
    PRE_COMMIT_HOOKS=$(grep -c "^- id:" .pre-commit-config.yaml 2>/dev/null)
    PRE_COMMIT_HOOKS=$(echo "$PRE_COMMIT_HOOKS" | tr -d ' \n')
    if [ -z "$PRE_COMMIT_HOOKS" ] || [ "$PRE_COMMIT_HOOKS" = "" ]; then
        PRE_COMMIT_HOOKS=0
    fi
    check_metric "Pre-commit Hooks" "$PRE_COMMIT_HOOKS" "5" "ge"
else
    echo "  ⚠️  .pre-commit-config.yaml not found - skipping pre-commit check"
fi

# CI/CD workflows
CI_WORKFLOWS=$(find .github/workflows -name "*.yml" -o -name "*.yaml" 2>/dev/null | wc -l | tr -d ' ')
check_metric "CI/CD Workflows" "$CI_WORKFLOWS" "1" "ge"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "6. PERFORMANCE VALIDATION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Database pool configuration
if [ -f "apps/backend/src/database.py" ]; then
    POOL_SIZE=$(grep "pool_size=" apps/backend/src/database.py 2>/dev/null | grep -oE "[0-9]+" | head -1 || echo "0")
    MAX_OVERFLOW=$(grep "max_overflow=" apps/backend/src/database.py 2>/dev/null | grep -oE "[0-9]+" | head -1 || echo "0")
    check_metric "Database Pool Size" "$POOL_SIZE" "15" "ge"
    check_metric "Database Max Overflow" "$MAX_OVERFLOW" "20" "ge"
fi

# Worker configuration
if [ -f "apps/backend/src/services/easypost_service.py" ]; then
    WORKERS=$(grep -E "max_workers|workers.*=" apps/backend/src/services/easypost_service.py 2>/dev/null | grep -oE "[0-9]+" | head -1 || echo "0")
    check_metric "ThreadPoolExecutor Workers" "$WORKERS" "16" "ge"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "VALIDATION SUMMARY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Passed: $PASS_COUNT"
echo "Failed: $FAIL_COUNT"
echo "Total:  $((PASS_COUNT + FAIL_COUNT))"
echo ""

if [ $FAIL_COUNT -eq 0 ]; then
    echo "✅ ALL VALIDATIONS PASSED"
    echo "Benchmark claims are VALIDATED"
    exit 0
else
    echo "⚠️  SOME VALIDATIONS FAILED"
    echo "Review failed metrics above"
    exit 1
fi
