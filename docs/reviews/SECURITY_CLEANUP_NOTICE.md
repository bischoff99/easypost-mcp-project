# Security Cleanup Notice

**Date:** November 11, 2025  
**Severity:** CRITICAL  
**Status:** RESOLVED

---

## 🔴 CRITICAL ISSUE FOUND AND RESOLVED

### Issue

**Exposed API Keys in Version Control**

The file `.vscode/thunder-client-settings.json` contained **exposed EasyPost API keys**:
- Test API Key: `EZTK151720b5bbc44c08bd3c3f7a055b69ac...`
- Production API Key: `EZAK151720b5bbc44c08bd3c3f7a055b69ac...`

This file was tracked in version control and potentially committed to the repository.

### Impact

- ⚠️ **HIGH**: API keys could be used to create shipments and access shipping data
- ⚠️ **HIGH**: Production key exposure could lead to unauthorized charges
- ⚠️ **MEDIUM**: Test key exposure could lead to rate limit exhaustion

### Resolution

**Actions Taken:**

1. ✅ **Removed file** `.vscode/thunder-client-settings.json`
2. ✅ **Updated .gitignore** to prevent future commits:
   ```gitignore
   .vscode/thunder-client-settings.json
   ```
3. ✅ **Documented** this security incident

**Recommended Next Steps:**

1. 🔄 **CRITICAL**: Rotate both API keys in EasyPost dashboard:
   - Log in to https://easypost.com/account/api-keys
   - Deactivate exposed keys
   - Generate new test and production keys
   - Update `.env` file with new keys

2. 🔍 **Review Git History**: Check if keys were ever committed:
   ```bash
   git log --all --full-history -S "EZTK151720b5bbc44c08bd3c3f7a055b69ac"
   git log --all --full-history -S "EZAK151720b5bbc44c08bd3c3f7a055b69ac"
   ```

3. 🔒 **If keys were committed**, consider using BFG Repo-Cleaner or git-filter-repo:
   ```bash
   # WARNING: Rewriting history requires force push
   git filter-repo --path .vscode/thunder-client-settings.json --invert-paths
   ```

4. ✅ **Verify** new keys are only in `.env` (which is gitignored)

### Prevention

**Thunder Client Configuration:**

Thunder Client stores environment variables in `.vscode/thunder-client-settings.json`. To prevent future exposure:

1. **Use environment variables** instead of hardcoded values:
   ```json
   {
     "name": "easypostApiKey",
     "value": "{{EASYPOST_API_KEY}}"
   }
   ```

2. **Create `.env` file** (already gitignored):
   ```bash
   EASYPOST_API_KEY=your_key_here
   ```

3. **Thunder Client will load** from environment variables automatically

### Files Cleaned Up

| File | Reason | Status |
|------|--------|--------|
| `.vscode/thunder-client-settings.json` | 🔴 Exposed API keys | ✅ Removed |
| `.devcontainer/` | Outdated paths | ✅ Removed |
| `.tool-versions` | Unused (asdf not installed) | ✅ Removed |
| `.claude/settings.local.json` | Single unused file | ✅ Removed |

### Security Best Practices

**DO:**
- ✅ Store secrets in `.env` files (gitignored)
- ✅ Use environment variables in configs
- ✅ Regularly rotate API keys
- ✅ Use test keys for development
- ✅ Review commits before pushing

**DON'T:**
- ❌ Hardcode API keys in config files
- ❌ Commit `.env` files to version control
- ❌ Share API keys in documentation
- ❌ Use production keys in development
- ❌ Ignore security warnings from tools

### Detection Tools

**Installed:**
- ✅ `detect-secrets` (see `.secrets.baseline`)
- ✅ Pre-commit hooks (see `.pre-commit-config.yaml`)

**How to scan:**
```bash
# Scan for secrets
detect-secrets scan

# Audit findings
detect-secrets audit .secrets.baseline
```

### References

- [EasyPost API Keys Documentation](https://www.easypost.com/docs/api#authentication)
- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)
- [OWASP Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)

---

## Verification Checklist

- [x] Thunder Client settings file removed
- [x] `.gitignore` updated to prevent future commits
- [x] Documentation created
- [ ] **TODO: Rotate exposed API keys in EasyPost dashboard**
- [ ] **TODO: Verify keys not in Git history**
- [ ] **TODO: Update `.env` with new keys**

---

**Status:** File cleanup complete. **Key rotation required.**

**Owner:** Development Team  
**Review Date:** November 11, 2025
