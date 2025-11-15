from __future__ import annotations

import os

import pytest

from src.utils import config


def _no_env_load() -> None:
    """Helper to bypass actual .env loading during tests."""
    return None


def _clear_env(*keys: str) -> None:
    for key in keys:
        os.environ.pop(key, None)


def setup_function(_):
    config.get_settings.cache_clear()


def test_build_settings_requires_api_key(monkeypatch):
    monkeypatch.setattr(config, "_initialise_environment", _no_env_load)
    _clear_env("EASYPOST_API_KEY")
    with pytest.raises(ValueError):
        config._build_settings()


def test_build_settings_parses_values(monkeypatch):
    monkeypatch.setattr(config, "_initialise_environment", _no_env_load)
    monkeypatch.setenv("EASYPOST_API_KEY", "key")
    monkeypatch.setenv("MCP_PORT", "9001")
    monkeypatch.setenv("CORS_ORIGINS", "https://example.com, http://localhost:3000")
    monkeypatch.setenv("CORS_ALLOW_METHODS", "GET,POST")
    monkeypatch.setenv("CORS_ALLOW_CREDENTIALS", "false")
    monkeypatch.setenv("MAX_BULK_CONCURRENCY", "8")

    settings = config._build_settings()

    assert settings.MCP_PORT == 9001
    assert settings.CORS_ORIGINS == ("https://example.com", "http://localhost:3000")
    assert settings.CORS_ALLOW_METHODS == ("GET", "POST")
    assert settings.CORS_ALLOW_CREDENTIALS is False
    assert settings.MAX_BULK_CONCURRENCY == 8
