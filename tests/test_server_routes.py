"""Smoke tests covering the public FastAPI surface and MCP mount."""

from __future__ import annotations

from fastapi import FastAPI

from src.server import app


def test_root_endpoint_reports_metadata(client):
    response = client.get("/")
    assert response.status_code == 200
    payload = response.json()
    assert payload["message"] == "EasyPost MCP Server"
    assert payload["docs"] == "/docs"
    assert payload["health"] == "/health"


def test_health_endpoint_is_ok(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"ok": True}


def test_mcp_mount_registered() -> None:
    """Ensure the FastAPI application mounts the MCP HTTP transport."""
    assert isinstance(app, FastAPI)
    mount_paths = {getattr(route, "path", None) for route in app.router.routes}
    assert "/mcp" in mount_paths
