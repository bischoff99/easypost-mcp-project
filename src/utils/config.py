import logging
import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = PROJECT_ROOT / "config"
ROOT_ENV = PROJECT_ROOT / ".env"
LOCAL_ENV = CONFIG_DIR / ".env"


def _load_env_file(path: Path, *, override: bool) -> bool:
    """Load an env file if present and return True when loaded."""
    if not path.exists():
        return False
    load_dotenv(path, override=override)
    logger.debug("Loaded config file: %s (override=%s)", path, override)
    return True


def _initialise_environment() -> None:
    """
    Load environment files in a predictable order:
    1. Root `.env` (optional, for shared overrides)
    2. Environment-specific file (`config/.env.<env>`)
    3. Local overrides (`config/.env`)
    """
    _load_env_file(ROOT_ENV, override=False)

    env_name = os.getenv("ENVIRONMENT", "development")
    env_file = CONFIG_DIR / f".env.{env_name}"
    _load_env_file(env_file, override=False)

    _load_env_file(LOCAL_ENV, override=True)


def _parse_bool(value: str | None, *, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "t", "yes", "y"}


def _parse_csv(value: str | None, *, default: str) -> tuple[str, ...]:
    raw = value if value is not None else default
    return tuple(item.strip() for item in raw.split(",") if item.strip())


@dataclass(frozen=True, slots=True)
class Settings:
    EASYPOST_API_KEY: str
    MCP_HOST: str
    MCP_PORT: int
    MCP_LOG_LEVEL: str
    CORS_ORIGINS: tuple[str, ...]
    CORS_ALLOW_CREDENTIALS: bool
    CORS_ALLOW_METHODS: tuple[str, ...]
    CORS_ALLOW_HEADERS: tuple[str, ...]
    ENVIRONMENT: str
    MAX_BULK_CONCURRENCY: int

    def validate(self) -> None:
        if not self.EASYPOST_API_KEY:
            raise ValueError("EASYPOST_API_KEY is required")


def _build_settings() -> Settings:
    _initialise_environment()

    settings = Settings(
        EASYPOST_API_KEY=os.getenv("EASYPOST_API_KEY", ""),
        MCP_HOST=os.getenv("MCP_HOST", "0.0.0.0"),  # noqa: S104 - required for Docker/dev
        MCP_PORT=int(os.getenv("MCP_PORT", "8000")),
        MCP_LOG_LEVEL=os.getenv("MCP_LOG_LEVEL", "INFO"),
        CORS_ORIGINS=_parse_csv(os.getenv("CORS_ORIGINS"), default="http://localhost:8000"),
        CORS_ALLOW_CREDENTIALS=_parse_bool(os.getenv("CORS_ALLOW_CREDENTIALS"), default=True),
        CORS_ALLOW_METHODS=_parse_csv(os.getenv("CORS_ALLOW_METHODS"), default="GET,POST,OPTIONS"),
        CORS_ALLOW_HEADERS=(
            "Content-Type",
            "Authorization",
            "X-Request-ID",
            "Accept",
            "Origin",
        ),
        ENVIRONMENT=os.getenv("ENVIRONMENT", "development"),
        MAX_BULK_CONCURRENCY=int(os.getenv("MAX_BULK_CONCURRENCY", "16")),
    )
    settings.validate()
    return settings


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached Settings instance."""
    return _build_settings()


settings = get_settings()
