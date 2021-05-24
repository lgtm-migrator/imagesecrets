"""Test the register request in the users router."""
from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    "username, email, password",
    [("string", "user@example.com", "pass"), ("123456", "user@string.com", "secret!!")],
)
def test_ok(api_client: TestClient, username: str, email: str, password: str) -> None:
    """Test successful post request on the register route."""
    response = api_client.post(
        "/users/register",
        json={"username": username, "email": email, "password": password},
    )
    response.raise_for_status()
    assert response.status_code == 201
    assert response.reason == "Created"
    json_ = response.json()
    assert json_["username"] == username
    assert json_["email"] == email
    with pytest.raises(KeyError):
        _ = json_["password"]
    assert not json_["decoded_images"]
    assert not json_["encoded_images"]


@pytest.mark.parametrize("username", ["string", "duplicate_username"])
def test_409(api_client: TestClient, username: str) -> None:
    """Test failing post request with a 409 status code (db conflict)."""
    from image_secrets.backend.database.user.models import User

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        User.create(username=username, email="...", password_hash="..."),
    )

    response = api_client.post(
        "/users/register",
        json={
            "username": username,
            "email": "user@example.com",
            "password": "string",
        },
    )

    assert response.status_code == 409
    assert response.reason == "Conflict"
    json_ = response.json()
    assert json_["detail"] == "account detail already exists"
    assert "UNIQUE constraint" in json_["field"]
    assert "username" in json_["value"]
