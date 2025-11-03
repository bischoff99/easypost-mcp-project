import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    # EasyPost
    EASYPOST_API_KEY: str = os.getenv("EASYPOST_API_KEY", "")

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
