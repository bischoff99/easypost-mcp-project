# EasyPost API Key Management with macOS Keychain

This document explains how EasyPost API keys are securely managed using macOS Keychain.

## Overview

Instead of storing API keys in plain text `.env` files, we use macOS Keychain for secure storage. Keys are automatically loaded based on the `ENVIRONMENT` variable.

## Setup

### 1. Store Keys in Keychain

```bash
# Test API key (for development)
security add-generic-password -s "easypost-test" -a "${USER}" -w "YOUR_TEST_KEY"

# Production API key (when ready)
security add-generic-password -s "easypost-prod" -a "${USER}" -w "YOUR_PROD_KEY"
```

### 2. Enable direnv (if not already enabled)

```bash
# Install direnv
brew install direnv

# Add to shell (zsh)
echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc
source ~/.zshrc

# Allow project directory
cd /path/to/easypost-mcp-project
direnv allow
```

## How It Works

### Automatic Loading via .envrc

The [.envrc](../../.envrc) file automatically:

1. Loads base configuration from `.env` files
2. Determines environment (test/production) from `ENVIRONMENT` variable
3. Loads appropriate API key from Keychain:
   - **Test environment** (default): Loads from `easypost-test`
   - **Production environment**: Loads from `easypost-prod`

### Environment Files

- **[config/.env](../../config/.env)**: Base configuration (no secrets)
- **[config/.env.test](../../config/.env.test)**: Test environment config (no hardcoded keys)
- **[config/.env.production](../../config/.env.production)**: Production config (no hardcoded keys)

## Usage

### Development (Test API Key)

```bash
# Default behavior - uses test key
make dev

# Or manually
source venv/bin/activate
uvicorn src.server:app --reload
```

### Production (Production API Key)

```bash
# Set environment to production
export ENVIRONMENT=production
make prod

# Or with docker
ENVIRONMENT=production make prod-docker
```

## Verifying Setup

```bash
# Check if key is loaded
eval "$(direnv export zsh)"
echo $EASYPOST_API_KEY

# Should show EZTK... for test or EZAK... for production
```

## Security Benefits

✅ **No hardcoded secrets** in version control
✅ **Encrypted storage** via macOS Keychain
✅ **User-specific** keys (tied to your macOS account)
✅ **Automatic cleanup** when leaving project directory
✅ **Environment-specific** key loading (test/prod separation)

## Helper Functions in ~/.zshrc

Your shell also has convenience functions:

```bash
# Load EasyPost production key
easypost_api_key

# Load EasyPost test key
easypost_test_key

# Load database URL from keychain
easypost_database_url
```

These functions use the same Keychain entries and can be called manually if needed.

## Troubleshooting

### Key not loading

```bash
# Check if key exists in Keychain
security find-generic-password -s "easypost-test" -w

# If not found, add it:
security add-generic-password -s "easypost-test" -a "${USER}" -w "YOUR_KEY"
```

### Wrong environment

```bash
# Check current environment
echo $ENVIRONMENT

# Set explicitly
export ENVIRONMENT=test  # or production
direnv reload
```

### direnv not working

```bash
# Re-allow directory
direnv allow

# Check status
direnv status
```

## Migration from Hardcoded Keys

If you previously had keys in `.env` files:

1. **Extract the key** from the old file
2. **Store in Keychain** using commands above
3. **Remove from .env** file (already done in this project)
4. **Test the setup** with `direnv reload`

## References

- [direnv documentation](https://direnv.net/)
- [macOS Keychain Access Guide](https://support.apple.com/guide/keychain-access/)
- [EasyPost API Keys](https://www.easypost.com/account/api-keys)
