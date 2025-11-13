import logging
import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

# Configure logger
logger = logging.getLogger(__name__)

# Load environment files in priority order:
# 1. Project root .env (base config, may contain ENVIRONMENT)
# 2. .env.production or .env.development (environment-specific, based on ENVIRONMENT from step 1)
# 3. .env (local overrides, highest priority)
backend_dir = Path(__file__).parent.parent.parent

# Step 1: Load project root .env first (to get ENVIRONMENT if set)
root_env = backend_dir.parent.parent / ".env"
if root_env.exists():
    load_dotenv(root_env, override=False)
    logger.info(f"Loaded root config: {root_env}")

# Step 2: Determine environment and load environment-specific file
env = os.getenv("ENVIRONMENT", "development")
env_specific = backend_dir / f".env.{env}"
if env_specific.exists():
    load_dotenv(env_specific, override=False)
    logger.info(f"Loaded environment-specific config: {env_specific}")

# Step 3: Load local .env last (overrides everything)
local_env = backend_dir / ".env"
if local_env.exists():
    load_dotenv(local_env, override=True)
    logger.info(f"Loaded local config: {local_env}")


class Settings:
    # EasyPost
    EASYPOST_API_KEY: str = os.getenv("EASYPOST_API_KEY", "")

    # Server
    MCP_HOST: str = os.getenv("MCP_HOST", "0.0.0.0")  # noqa: S104 - Required for Docker
    MCP_PORT: int = int(os.getenv("MCP_PORT", "8000"))
    MCP_LOG_LEVEL: str = os.getenv("MCP_LOG_LEVEL", "INFO")

    # CORS
    CORS_ORIGINS: list = [
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS", "http://localhost:5173,http://localhost:4173"
        ).split(",")
        if origin.strip()
    ]
    CORS_ALLOW_CREDENTIALS: bool = os.getenv("CORS_ALLOW_CREDENTIALS", "true").lower() == "true"
    CORS_ALLOW_METHODS: list = os.getenv("CORS_ALLOW_METHODS", "GET,POST,OPTIONS").split(",")
    CORS_ALLOW_HEADERS: list = [
        "Content-Type",
        "Authorization",
        "X-Request-ID",
        "Accept",
        "Origin",
    ]

    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    # Bulk operations concurrency (M3 Max: 16 cores)
    MAX_BULK_CONCURRENCY: int = int(os.getenv("MAX_BULK_CONCURRENCY", "16"))

    def validate(self):
        """Validate required configuration."""
        errors = []

        if not self.EASYPOST_API_KEY:
            errors.append("EASYPOST_API_KEY is required")

        if errors:
            raise ValueError(f"Configuration errors: {'; '.join(errors)}")

        return True


@lru_cache
def get_settings() -> Settings:
    """
    Get cached settings instance.

    FastAPI best practice: Use @lru_cache to ensure Settings is instantiated
    only once and reused across the application lifecycle.

    Returns:
        Settings: Cached application settings
    """
    return Settings()


# Backwards compatibility: Module-level instance for non-dependency use
settings = get_settings()
