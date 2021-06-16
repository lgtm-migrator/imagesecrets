"""Test the user api router without account authentication."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from requests import HTTPError

if TYPE_CHECKING:
    from fastapi.testclient import TestClient

URL = "/users/me"


def test_get(api_client: TestClient) -> None:
    """Test the get request."""
    response = api_client.get(URL)
    with pytest.raises(HTTPError):
        response.raise_for_status()
    assert response.status_code == 401
    assert response.reason == "Unauthorized"
    assert response.headers["www-authenticate"] == "Bearer"
    assert response.json()["detail"] == "invalid access token"


def test_patch(api_client: TestClient) -> None:
    """Test the patch request."""
    response = api_client.patch(
        URL,
        json={"username": "string", "email": "user@example.com"},
    )
    with pytest.raises(HTTPError):
        response.raise_for_status()
    assert response.status_code == 401
    assert response.reason == "Unauthorized"
    assert response.headers["www-authenticate"] == "Bearer"
    assert response.json()["detail"] == "invalid access token"


def test_delete(api_client: TestClient) -> None:
    """Test the delete request."""
    response = api_client.delete(
        URL,
        json={"username": "string", "email": "user@example.com"},
    )
    with pytest.raises(HTTPError):
        response.raise_for_status()
    assert response.status_code == 401
    assert response.reason == "Unauthorized"
    assert response.headers["www-authenticate"] == "Bearer"
    assert response.json()["detail"] == "invalid access token"


def test_password_put(api_client) -> None:
    """Test put request for password endpoint."""
    response = api_client.put(
        f"{URL}/password",
        json={"old": "old_password", "new": "new_password"},
    )

    with pytest.raises(HTTPError):
        response.raise_for_status()
    assert response.status_code == 401
    assert response.reason == "Unauthorized"
    assert response.headers["www-authenticate"] == "Bearer"
    assert response.json()["detail"] == "invalid access token"
