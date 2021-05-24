"""Test the home route."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi.testclient import TestClient


def test_get(api_client: TestClient, app_name) -> None:
    """Test the get request on the home route."""
    response = api_client.get("/")
    response.raise_for_status()
    assert response.status_code == 200
    assert response.json() == {"app-name": app_name}


__all__ = [
    "test_get",
]
