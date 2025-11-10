# Project Structure Review & Cleanup Plan

## Root Directory Analysis

### Current Root Files (7 markdown files)
1. ✅ `README.md` - Main project README (KEEP)
2. ✅ `CLAUDE.md` - AI assistant guide (KEEP)
3. ✅ `CONTRIBUTING.md` - Contribution guidelines (KEEP)
4. ✅ `SECURITY.md` - Security documentation (KEEP)
5. ⚠️ `CHANGES_2025-11-10.md` - Today's changes (MOVE to docs/changelog/)
6. ⚠️ `CLEANUP_SUMMARY_2025-11-10.md` - Today's cleanup (MOVE to docs/changelog/)
7. ⚠️ `STRUCTURE_CLEANUP_2025-11-10.md` - Today's structure work (MOVE to docs/changelog/)

### Issues Found

1. **Temporary Documentation in Root**
   - 3 cleanup/summary files should be archived
   - Should consolidate into single changelog entry

2. **shipping-labels Directory**
   - Contains production shipping labels
   - Should be in .gitignore (already has `labels/` but not `shipping-labels/`)

3. **Documentation Duplication**
   - Multiple review files with similar content
   - `docs/reviews/` has both `archive/` and `archived-reviews/` subdirectories
   - Some files appear in multiple locations

4. **Unused Files**
   - Old test scripts in `backend/tests/manual/`
   - Captured responses that may be outdated

## Cleanup Actions

### Priority 1: Root Directory Cleanup
- [ ] Move cleanup summaries to `docs/changelog/2025-11-10/`
- [ ] Update .gitignore for shipping-labels
- [ ] Consolidate duplicate documentation

### Priority 2: Documentation Organization
- [ ] Consolidate review archives
- [ ] Create clear documentation index
- [ ] Remove truly outdated files

### Priority 3: Code Structure
- [ ] Verify all imports are correct
- [ ] Check for unused dependencies
- [ ] Ensure consistent code style
