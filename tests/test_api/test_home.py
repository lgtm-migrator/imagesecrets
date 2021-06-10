"""Test the home route."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi.testclient import TestClient

    from image_secrets.api.config import Settings


def test_get(api_client: TestClient, api_settings: Settings) -> None:
    """Test get request on the home route."""
    response = api_client.get("/")

    response.raise_for_status()
    assert response.status_code == 200
    assert response.json() == {
        "AppName": api_settings.app_name,
        "SwaggerUI": api_settings.swagger_url,
        "ReDoc": api_settings.redoc_url,
        "GitLab": api_settings.repository_url,
    }


__all__ = [
    "test_get",
]
