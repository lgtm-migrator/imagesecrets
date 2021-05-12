"""Test the encode route."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi.testclient import TestClient


def test_get(api_client: TestClient, api_name) -> None:
    """Test the get request of the encode route."""
    response = api_client.get("/encode/")
    assert response.status_code == 200
    assert response.json() == {"app-name": api_name}
