# Security Alert: API Keys in Git History

**Date**: 2025-11-12  
**Severity**: 🔴 **CRITICAL**  
**Status**: ⚠️ **ACTION REQUIRED**

---

## Issue Summary

**API keys were found in Git history** - they were committed to the repository.

### Exposure Details

- **Test API Key**: Found in **24 commits**
- **Production API Key**: Found in **2 commits**
- **Keys**: `EZTK151720b5bbc44c08bd3c3f7a055b69ac` and `EZAK151720b5bbc44c08bd3c3f7a055b69ac`

### Impact

- 🔴 **CRITICAL**: Anyone with repository access can extract keys from git history
- 🔴 **CRITICAL**: Keys can be used to create shipments and access shipping data
- 🔴 **CRITICAL**: Production key exposure could lead to unauthorized charges
- 🟡 **HIGH**: Test key exposure could lead to rate limit exhaustion

---

## Immediate Actions Required

### 1. Rotate API Keys (URGENT - Do This Now)

1. Log in to https://easypost.com/account/api-keys
2. **Deactivate** both exposed keys immediately:
   - Test key: `EZTK151720b5bbc44c08bd3c3f7a055b69ac`
   - Production key: `EZAK151720b5bbc44c08bd3c3f7a055b69ac`
3. **Generate new keys**:
   - New test key
   - New production key
4. **Update `.env` file** with new keys:
   ```bash
   EASYPOST_API_KEY=your_new_test_key_here
   EASYPOST_PRODUCTION_API_KEY=your_new_production_key_here
   ```

### 2. Clean Git History (Required for Security)

**Option A: Use git-filter-repo (Recommended)**

```bash
# Install git-filter-repo if needed
pip install git-filter-repo

# Remove file containing keys from all history
git filter-repo --path .vscode/thunder-client-settings.json --invert-paths

# Force push (WARNING: This rewrites history)
git push origin --force --all
```

**Option B: Use BFG Repo-Cleaner**

```bash
# Download BFG from https://rtyley.github.io/bfg-repo-cleaner/
java -jar bfg.jar --delete-files thunder-client-settings.json
git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push origin --force --all
```

**⚠️ WARNING**: Rewriting git history requires force push and affects all collaborators.

### 3. Verify Keys Removed

After cleaning history:

```bash
# Verify keys no longer in history
git log --all --full-history -S "EZTK151720b5bbc44c08bd3c3f7a055b69ac"
git log --all --full-history -S "EZAK151720b5bbc44c08bd3c3f7a055b69ac"

# Should return no results
```

---

## Prevention

### Already Implemented ✅

1. ✅ `.vscode/thunder-client-settings.json` removed from repository
2. ✅ Added to `.gitignore` to prevent future commits
3. ✅ `detect-secrets` configured in `.secrets.baseline`
4. ✅ Pre-commit hooks configured

### Best Practices

- ✅ Store secrets in `.env` files (gitignored)
- ✅ Use environment variables in configs
- ✅ Regularly rotate API keys
- ✅ Use test keys for development
- ✅ Review commits before pushing
- ✅ Run `detect-secrets scan` before committing

---

## Timeline

- **2025-11-11**: Keys exposed in `.vscode/thunder-client-settings.json`
- **2025-11-11**: File removed and added to `.gitignore`
- **2025-11-12**: Keys found in git history (24 commits with test key, 2 with production key)
- **2025-11-12**: This document created

---

## References

- [EasyPost API Keys Documentation](https://www.easypost.com/docs/api#authentication)
- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)
- [OWASP Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [git-filter-repo Documentation](https://github.com/newren/git-filter-repo)

---

**Status**: ⚠️ **Keys must be rotated and git history cleaned**

**Owner**: Development Team  
**Priority**: 🔴 **CRITICAL**

