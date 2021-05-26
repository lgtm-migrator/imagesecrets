"""Test the user api router without account authentication."""

import pytest
from requests import HTTPError


def test_get(api_client) -> None:
    """Test the get request."""
    response = api_client.get("/users/me")
    with pytest.raises(HTTPError):
        response.raise_for_status()
    assert response.status_code == 401
    assert response.reason == "Unauthorized"
    assert response.headers["www-authenticate"] == "Bearer"
    assert response.json()["detail"] == "invalid access token"


def test_patch(api_client) -> None:
    """Test the patch request."""
    response = api_client.patch(
        "/users/me",
        json={"username": "string", "email": "user@example.com"},
    )
    with pytest.raises(HTTPError):
        response.raise_for_status()
    assert response.status_code == 401
    assert response.reason == "Unauthorized"
    assert response.headers["www-authenticate"] == "Bearer"
    assert response.json()["detail"] == "invalid access token"


def test_delete(api_client) -> None:
    """Test the delete request."""
    response = api_client.delete(
        "/users/me",
        json={"username": "string", "email": "user@example.com"},
    )
    with pytest.raises(HTTPError):
        response.raise_for_status()
    assert response.status_code == 401
    assert response.reason == "Unauthorized"
    assert response.headers["www-authenticate"] == "Bearer"
    assert response.json()["detail"] == "invalid access token"
