# Shell Environment Setup

## Quick Reference

Your shell configuration has been updated to support the dual MCP environment setup.

### Shell Aliases (Available After Reload)

```bash
# Check current environment
ep-status

# Switch to test environment (safe, default)
ep-test

# Switch to production environment (⚠️ real charges)
ep-prod
```

### Usage Examples

**Daily Development:**

```bash
# Start new terminal (defaults to test)
cd ~/Projects/personal/easypost-mcp-project
ep-status
# Output: Current environment: test

# Work with test API
uvicorn src.server:app --reload
# Uses config/.env.test → EZTK key
```

**Production Testing:**

```bash
# Explicitly switch to production
ep-prod
# Output: ⚠️  EasyPost: PRODUCTION environment (EZAK key)

# Run with production key
uvicorn src.server:app --reload
# Uses config/.env.production → EZAK key
```

**Switch Back:**

```bash
ep-test
# Output: ✓ EasyPost: TEST environment (EZTK key)
```

## Activation

Reload your shell configuration:

```bash
# Reload zsh config
source ~/.zshrc

# Or open new terminal window
```

## Environment Variable Priority

1. **Shell export** (highest): `export ENVIRONMENT=test`
2. **Direnv (.envrc)**: Loads from `.env.test` or `.env.production`
3. **Environment files**: `.env.test` and `.env.production`
4. **Default**: `test` (safe default)

## Verification

```bash
# Check what environment is active
echo "ENVIRONMENT: $ENVIRONMENT"

# Check within project (with direnv)
cd ~/Projects/personal/easypost-mcp-project
python -c "from src.utils.config import settings; print(f'Environment: {settings.ENVIRONMENT}'); print(f'API Key: {settings.EASYPOST_API_KEY[:4]}...')"
```

Expected output:

```
Environment: test
API Key: EZTK...
```

## Configuration Location

Shell configuration: `~/.zshrc` (lines 272-285)

Changes made:

- ✓ Removed old `EASYPOST_ENVIRONMENT` and `EASYPOST_LOG_LEVEL` exports
- ✓ Added `ENVIRONMENT` with safe default (test)
- ✓ Added convenience aliases for switching
- ✓ Documented keychain loader functions (still available)

## Related Documentation

- [MCP Environment Switching](../guides/MCP_ENVIRONMENT_SWITCHING.md)
- [Environment Setup](./ENVIRONMENT_SETUP.md)
