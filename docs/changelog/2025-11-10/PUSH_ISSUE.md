# Push Issue - API Key in Commit History

## Problem

GitHub's push protection detected production API keys in commit `3df8878`:

**Detected secrets:**
- `.cursor/mcp.json:7`
- `.cursor/rest-client-environments.json:14`
- `.thunder-client/thunder-environment.json:55`
- `docs/reviews/RATES_FIX_SUMMARY.md:85`
- `docs/reviews/archived-reviews/MCP_DIAGNOSTIC.md:42`

**Error:**
```
remote: - Push cannot contain secrets
remote: —— EasyPost Production API Key ———————————————————————
```

## Root Cause

Production API key `your_production_api_key_here...` was committed in:
- Commit `3df8878` - Initial international shipping implementation
- Configuration files and documentation

## Solutions

### Option 1: Use GitHub's Bypass URL ⚠️
**Not recommended** - Leaves API key in git history

```bash
# Open GitHub's allow URL
open "https://github.com/bischoff99/easypost-mcp-project/security/secret-scanning/unblock-secret/35FrnndKI3SX6Cxzqpi1T5BoUs8"
# Click "Allow secret" button
# Then push normally
git push origin feature/international-shipping
```

### Option 2: Rewrite Git History ✅ **Recommended**

Remove API key from all commits using BFG or git filter-repo:

**Using BFG Repo-Cleaner:**
```bash
# Install BFG
brew install bfg

# Create backup
git clone /Users/andrejs/Developer/github/andrejs/easypost-mcp-project /tmp/easypost-backup

# Remove API key from all commits
cd /Users/andrejs/Developer/github/andrejs/easypost-mcp-project
bfg --replace-text <(echo 'your_production_api_key_here===>your_production_api_key_here')

# Clean up
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Force push (history rewritten)
git push origin feature/international-shipping --force
```

**Using git filter-repo:**
```bash
# Install git-filter-repo
brew install git-filter-repo

# Remove API key from history
git filter-repo --replace-text <(echo 'your_production_api_key_here==>your_production_api_key_here')

# Force push
git push origin feature/international-shipping --force
```

### Option 3: Squash Commits ✅ **Simplest**

Create a single squashed commit with API keys already removed:

```bash
# Reset to base commit
git checkout -b feature/international-shipping-v2 9dcd776

# Apply all changes from master
git merge master --squash

# Ensure API keys are removed (already done)
# Commit with clean history
git commit -m "feat(shipping): international shipping improvements and comprehensive cleanup"

# Push new clean branch
git push origin feature/international-shipping-v2

# Create PR
gh pr create --base master --head feature/international-shipping-v2 \
  --title "feat: International Shipping Improvements" \
  --body "Comprehensive shipping improvements with DDP/DDU support"
```

## Current Status

**Branch:** `feature/international-shipping-clean` (same as master)
**Issue:** Commit `3df8878` contains API keys in history
**Latest commit:** `5f2e09e` (API keys removed, but still in history)

## Recommended Action

Use Option 3 (Squash) - cleanest and simplest solution.

## Files to Review Before Push

Ensure these files have placeholders, not actual API keys:
- `.cursor/mcp.json`
- `.cursor/rest-client-environments.json`
- `.thunder-client/thunder-environment.json`
- All files in `docs/`

## Security Best Practices

1. **Never commit API keys** - Use `.env` files (already in `.gitignore`)
2. **Use environment variables** - Reference `EASYPOST_API_KEY` from env
3. **Review before commit** - Check `git diff` for secrets
4. **Enable pre-commit hooks** - Add secret detection
5. **Rotate compromised keys** - If pushed, immediately regenerate

## Next Steps

1. Choose solution (recommend Option 3)
2. Execute cleanup
3. Verify no secrets in new commits
4. Push to remote
5. **Regenerate API key** in EasyPost dashboard (security best practice)
