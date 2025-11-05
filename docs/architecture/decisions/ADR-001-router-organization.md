# ADR-001: Router Organization Strategy

**Date:** November 5, 2025
**Status:** Proposed
**Deciders:** Development Team

---

## Context

The FastAPI server.py file grew to 1231 lines with all endpoints defined in a single file. This makes maintenance difficult and violates separation of concerns.

## Decision

**Defer router refactoring until test suite is updated.**

**Rationale:**
- Current monolithic structure works well (111/111 tests pass)
- Router refactoring requires updating 100+ test files
- No immediate business need for the refactoring
- Code is already well-organized within the single file

**Future Path:**
1. Create router modules (✅ DONE - in src/routers/)
2. Update all test files to match new structure
3. Migrate frontend to use `/api/v1/*` endpoints
4. Activate router-based architecture
5. Add API versioning

## Consequences

### Positive
- Maintains 100% test pass rate
- No breaking changes for frontend
- Allows incremental migration
- Router code ready when needed

### Negative
- server.py remains large (1231 lines)
- Deferred technical debt
- No API versioning yet

## Alternatives Considered

1. **Immediate refactoring** - Rejected due to test update burden
2. **Gradual endpoint migration** - Rejected due to inconsistent structure during migration
3. **Current approach** - Accepted (defer until tests can be updated)

## Implementation

**Created:**
- `src/routers/shipments.py` - Shipment + rates endpoints
- `src/routers/tracking.py` - Tracking endpoints
- `src/routers/analytics.py` - Analytics endpoints
- `src/routers/database.py` - Database endpoints
- `src/routers/webhooks.py` - Webhook handlers
- `src/server-refactored.py` - Reference implementation

**Saved for future use** when tests can be updated.

---

**Next Review:** Q1 2026 or when test update sprint is scheduled

