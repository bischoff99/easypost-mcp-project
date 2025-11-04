import logging
import os
from pathlib import Path

from dotenv import load_dotenv

# Configure logger
logger = logging.getLogger(__name__)

# Determine which .env file to load based on ENVIRONMENT variable
env = os.getenv("ENVIRONMENT", "development")
env_file = Path(__file__).parent.parent.parent / f".env.{env}"

# Load environment-specific file if it exists, otherwise use .env
if env_file.exists():
    load_dotenv(env_file)
    logger.info(f"Loaded environment from: {env_file}")
else:
    load_dotenv()
    logger.info("Loaded environment from: .env")


class Settings:
    # EasyPost
    EASYPOST_API_KEY: str = os.getenv("EASYPOST_API_KEY", "")

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "postgresql://user:password@localhost/easypost_mcp"
    )
    # Connection pool settings (optimized for M3 Max)
    DATABASE_POOL_SIZE: int = int(os.getenv("DATABASE_POOL_SIZE", "20"))
    DATABASE_MAX_OVERFLOW: int = int(os.getenv("DATABASE_MAX_OVERFLOW", "30"))
    DATABASE_POOL_RECYCLE: int = int(os.getenv("DATABASE_POOL_RECYCLE", "3600"))
    DATABASE_POOL_TIMEOUT: int = int(os.getenv("DATABASE_POOL_TIMEOUT", "30"))
    DATABASE_COMMAND_TIMEOUT: int = int(os.getenv("DATABASE_COMMAND_TIMEOUT", "60"))
    DATABASE_CONNECT_TIMEOUT: int = int(os.getenv("DATABASE_CONNECT_TIMEOUT", "10"))

    # Server
    MCP_HOST: str = os.getenv("MCP_HOST", "0.0.0.0")
    MCP_PORT: int = int(os.getenv("MCP_PORT", "8000"))
    MCP_LOG_LEVEL: str = os.getenv("MCP_LOG_LEVEL", "INFO")

    # CORS
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
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

    def validate(self):
        if not self.EASYPOST_API_KEY:
            raise ValueError("EASYPOST_API_KEY is required")
        return True


settings = Settings()
