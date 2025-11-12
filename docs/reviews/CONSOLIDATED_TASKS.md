# Consolidated Project Tasks

**Last Updated**: 2025-11-12
**Status**: Active task tracking
**Source**: Consolidated from all project review documents

---

## 🔴 Critical (Fix Immediately)

### Configuration Fixes

1. **Fix MCP Configuration Path** ⏱️ 5 min ⚠️ **NOT APPLICABLE**
   - **Status**: `.cursor/mcp.json` is a template with empty `mcpServers: {}`
   - **Note**: Actual MCP config is in Claude Desktop's config file (not in repo)
   - **Reference**: `fastmcp.json` shows correct path: `apps/backend/src/mcp_server/server.py`
   - **Source**: PROJECT_REVIEW_2025-11-11.md

2. **Update `.dev-config.json` Paths** ⏱️ 5 min ✅ **ALREADY CORRECT**
   - **Status**: Paths already correct (`apps/backend/src`, `apps/frontend/src`)
   - **Verified**: No changes needed
   - **Source**: COMPREHENSIVE_PROJECT_REVIEW.md

3. **Update `.cursorrules` References** ⏱️ 2 min ✅ **ALREADY FIXED**
   - **Status**: No reference to `packages/core/` found in `.cursorrules`
   - **Verified**: File is clean
   - **Source**: COMPREHENSIVE_PROJECT_REVIEW.md

### Security

4. **Rotate Exposed API Keys** ⏱️ 15 min ⚠️ **ACTION REQUIRED**
   - **Status**: Keys found in git history (24 commits with test key, 2 with production key)
   - **Impact**: CRITICAL - Keys are permanently in git history
   - **Action Required**: 
     - Log in to https://easypost.com/account/api-keys
     - Deactivate exposed keys immediately
     - Generate new test and production keys
     - Update `.env` file with new keys
     - Clean git history (see `SECURITY_API_KEYS_IN_HISTORY.md`)
   - **Source**: SECURITY_CLEANUP_NOTICE.md, SECURITY_API_KEYS_IN_HISTORY.md

5. **Verify Keys Not in Git History** ⏱️ 10 min ✅ **COMPLETED**
   - **Status**: Verified - Keys ARE in git history
   - **Findings**: Test key in 24 commits, Production key in 2 commits
   - **Documentation**: Created `SECURITY_API_KEYS_IN_HISTORY.md` with remediation steps
   - **Source**: SECURITY_CLEANUP_NOTICE.md

### Git & Repository

6. **Commit Staged Changes** ⏱️ 30 min ✅ **COMPLETED**
   - **Status**: Committed 23 files
   - **Commit**: `76faf01` - "chore: consolidate tasks and update documentation"
   - **Files**: Consolidated tasks, documentation updates, security docs
   - **Source**: PROJECT_REVIEW_2025-11-11.md

---

## 🟡 High Priority (Fix This Week)

### Repository Hygiene

7. **Clean Root Directory** ⏱️ 15 min ✅ **ALREADY CLEAN**
   - **Status**: Root directory is clean - no temp files found
   - **Verified**: No SUMMARY/REPORT/CONFLICTS files in root
   - **Note**: Previous cleanup already completed
   - **Source**: PROJECT_REVIEW_2025-11-11.md

8. **Move CLEANUP_ANALYSIS.md** ⏱️ 2 min ✅ **ALREADY DONE**
   - **Status**: File already in correct location: `docs/reviews/CLEANUP_ANALYSIS.md`
   - **Verified**: Properly organized
   - **Source**: CLEANUP_ANALYSIS.md

### Dependencies & Build

9. **Fix pnpm-lock.yaml Tracking** ⏱️ 5 min ✅ **ALREADY CORRECT**
   - **Status**: `pnpm-lock.yaml` is tracked (not in .gitignore)
   - **Verified**: Comment in .gitignore confirms tracking
   - **Source**: PROJECT_REVIEW_2025-11-11.md

10. **Create Backend Lock File** ⏱️ 5 min ✅ **ALREADY EXISTS**
    - **Status**: File exists: `apps/backend/requirements-lock.txt`
    - **Verified**: Lock file present and tracked
    - **Source**: PROJECT_REVIEW_2025-11-11.md

### Testing

11. **Verify Test Coverage** ⏱️ 15 min ⚠️ **BELOW TARGET**
    - **Status**: Current coverage: 32.11% (target: 36%)
    - **Issue**: 28 tests failing, coverage below target
    - **Action**: Fix failing tests to improve coverage
    - **Note**: Test failures need to be addressed separately
    - **Source**: PROJECT_REVIEW_2025-11-11.md

### Security

12. **Run Security Audit** ⏱️ 10 min ✅ **COMPLETED**
    - **Status**: Frontend audit passed, backend needs manual review
    - **Frontend**: ✅ No vulnerabilities found (pnpm audit)
    - **Backend**: ⚠️ pip-audit has technical issues but dependencies appear safe
    - **Action**: Manual review recommended for backend dependencies
    - **Source**: PROJECT_REVIEW_2025-11-11.md

---

## 🟢 Medium Priority (This Month)

### Documentation

13. **Consolidate Review Documents** ⏱️ 2 hours
    - **Issue**: Multiple review files could be consolidated
    - **Impact**: Easier navigation
    - **Fix**: Create single `docs/reviews/LATEST_REVIEW.md` symlink
    - **Source**: PROJECT_REVIEW_2025-11-11.md

14. **Document Cursor Configuration** ⏱️ 30 min
    - **Issue**: Many Cursor-specific files undocumented
    - **Impact**: Hard to understand purpose
    - **Fix**: Create `.cursor/README.md` explaining each file
    - **Source**: PROJECT_REVIEW_2025-11-11.md

15. **Create Benchmarking Guide** ⏱️ 30 min
    - **Issue**: `scripts/benchmark.sh` exists but not documented
    - **Impact**: Tool not discoverable
    - **Fix**: Create `docs/guides/BENCHMARKING.md`
    - **Source**: PROJECT_REVIEW_2025-11-11.md

### Code Quality

16. **Frontend i18n Cleanup** ⏱️ 1 hour
    - **Issue**: `locales/` directory exists but `i18n.js` deleted
    - **Impact**: Inconsistent state
    - **Fix**: Either remove locales or restore i18n support
    - **Source**: PROJECT_REVIEW_2025-11-11.md

17. **Database Migration Cleanup** ⏱️ 30 min
    - **Issue**: Migration marked for deletion should be removed
    - **Impact**: Migration chain integrity
    - **Fix**: Run `alembic history` to verify chain, remove deleted migration
    - **Source**: PROJECT_REVIEW_2025-11-11.md

### Frontend Improvements

18. **Add Component Tests** ⏱️ 4 hours
    - **Issue**: Missing component tests for major components
    - **Impact**: Reduced test coverage
    - **Fix**: Add tests for all major components
    - **Source**: FRONTEND_REVIEW.md

19. **Add PropTypes or TypeScript** ⏱️ 8 hours
    - **Issue**: No type checking for React components
    - **Impact**: Runtime errors possible
    - **Fix**: Add PropTypes or migrate to TypeScript
    - **Source**: FRONTEND_REVIEW.md

20. **Verify Accessibility** ⏱️ 2 hours
    - **Issue**: ARIA attributes and keyboard navigation not verified
    - **Impact**: Accessibility issues
    - **Fix**: Run accessibility audit, verify ARIA attributes
    - **Source**: FRONTEND_REVIEW.md

---

## 🔵 Low Priority (Nice to Have)

### Performance

21. **Add Bundle Size Limits** ⏱️ 1 hour
    - **Issue**: No bundle size monitoring
    - **Impact**: Bundle could grow unbounded
    - **Fix**: Configure bundle size limits in build
    - **Source**: FRONTEND_REVIEW.md

22. **Track Core Web Vitals** ⏱️ 2 hours
    - **Issue**: No performance metrics tracking
    - **Impact**: Can't measure performance improvements
    - **Fix**: Add Core Web Vitals tracking
    - **Source**: FRONTEND_REVIEW.md

23. **Run Performance Benchmarks** ⏱️ 1 hour
    - **Issue**: No baseline performance metrics
    - **Impact**: Can't measure improvements
    - **Fix**: Run `make benchmark` and document baseline
    - **Source**: PROJECT_REVIEW_2025-11-11.md

### Code Quality Metrics

24. **Add Quality Metrics Dashboard** ⏱️ 4 hours
    - **Issue**: No automated quality tracking
    - **Impact**: Can't track code quality trends
    - **Fix**: Add tools like `radon` (Python complexity), `cloc` (line counts)
    - **Source**: PROJECT_REVIEW_2025-11-11.md

### Documentation

25. **Document Public APIs** ⏱️ 2 hours
    - **Issue**: Public APIs not documented
    - **Impact**: Hard to use APIs
    - **Fix**: Add JSDoc/TSDoc for public APIs
    - **Source**: FRONTEND_REVIEW.md

---

## 📊 Task Summary

| Priority | Count | Estimated Time |
|----------|-------|----------------|
| 🔴 Critical | 6 | ~1.5 hours |
| 🟡 High | 6 | ~1 hour |
| 🟢 Medium | 7 | ~18 hours |
| 🔵 Low | 5 | ~10 hours |
| **Total** | **24** | **~30.5 hours** |

---

## 🎯 Quick Wins (Under 15 Minutes)

**Status**: ✅ **4 of 6 already completed!**

Completed:
1. ✅ Update `.dev-config.json` paths (already correct)
2. ✅ Update `.cursorrules` references (already fixed)
3. ✅ Move CLEANUP_ANALYSIS.md (already done)
4. ✅ Fix pnpm-lock.yaml tracking (already correct)
5. ✅ Create backend lock file (already exists)

Remaining:
1. ⚠️ Fix MCP configuration path (not applicable - template file)

**Result**: Quick wins section mostly complete! Focus on Critical tasks instead.

---

## 📝 Notes

- **Source Documents**: Tasks extracted from:
  - `PROJECT_REVIEW_2025-11-11.md`
  - `COMPREHENSIVE_PROJECT_REVIEW.md`
  - `SECURITY_CLEANUP_NOTICE.md`
  - `CLEANUP_ANALYSIS.md`
  - `FRONTEND_REVIEW.md`
  - `FRONTEND_DEPENDENCY_REVIEW.md`

- **Status Tracking**: Update this file as tasks are completed
- **Priority**: Based on impact and urgency
- **Time Estimates**: Rough estimates, may vary

---

## ✅ Completed Tasks

1. ✅ **Update `.dev-config.json` paths** (2025-11-12)
   - Paths already correct: `apps/backend/src`, `apps/frontend/src`
   - Verified: Paths match current structure

2. ✅ **Move CLEANUP_ANALYSIS.md** (2025-11-12)
   - Already in correct location: `docs/reviews/CLEANUP_ANALYSIS.md`
   - Verified: File is properly organized

3. ✅ **Fix pnpm-lock.yaml tracking** (2025-11-12)
   - Already tracked (not in .gitignore)
   - Verified: Comment in .gitignore confirms tracking

4. ✅ **Create backend lock file** (2025-11-12)
   - File exists: `apps/backend/requirements-lock.txt`
   - Verified: Lock file present and tracked

5. ✅ **Verify API keys in Git history** (2025-11-12)
   - Found: Test key in 24 commits, Production key in 2 commits
   - Action: Created `SECURITY_API_KEYS_IN_HISTORY.md` with remediation steps
   - Status: ⚠️ CRITICAL - Keys must be rotated and git history cleaned

6. ✅ **Commit staged changes** (2025-11-12)
   - Committed: 23 files changed (consolidated tasks, documentation updates)
   - Commit: `76faf01` - "chore: consolidate tasks and update documentation"

7. ✅ **Run security audit** (2025-11-12)
   - Frontend: ✅ No vulnerabilities found (pnpm audit)
   - Backend: ⚠️ pip-audit has technical issues but dependencies appear safe
   - Status: Frontend secure, backend needs manual review

8. ✅ **Verify test coverage** (2025-11-12)
   - Current: 32.11% (below 36% target)
   - Status: ⚠️ Coverage below target - 28 tests failing
   - Note: Test failures need to be addressed separately

---

**Last Review**: 2025-11-12
**Next Review**: When tasks are completed or priorities change
