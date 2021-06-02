"""Test the user api router without account authentication."""

import pytest
from requests import HTTPError

URL = "/users/me"


def test_get(api_client) -> None:
    """Test the get request."""
    response = api_client.get(URL)
    with pytest.raises(HTTPError):
        response.raise_for_status()
    assert response.status_code == 401
    assert response.reason == "Unauthorized"
    assert response.headers["www-authenticate"] == "Bearer"
    assert response.json()["detail"] == "invalid access token"


def test_patch(api_client) -> None:
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


def test_delete(api_client) -> None:
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
