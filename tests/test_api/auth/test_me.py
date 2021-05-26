"""Test the me router with authenticated user."""
from __future__ import annotations

import asyncio
from json import JSONDecodeError
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from fastapi.testclient import TestClient

    from image_secrets.backend.database.user.models import User


URL = "/users/me"


def test_get(api_client: TestClient, auth_token: tuple[User, dict[str, str]]) -> None:
    """Test the get request."""
    token = auth_token[1]
    user = auth_token[0]
    response = api_client.get(
        URL,
        headers={
            "authorization": f'{token["token_type"].capitalize()} {token["access_token"]}',
        },
    )

    response.raise_for_status()
    assert response.status_code == 200
    assert response.reason == "OK"
    json_ = response.json()
    assert json_["username"] == user.username
    assert json_["email"] == user.email
    assert json_["created"] == json_["modified"]
    assert not json_["decoded_images"]
    assert not json_["encoded_images"]


@pytest.mark.parametrize(
    "username, email",
    [("test-name", "test@email.com"), ("123456", "example@result.com")],
)
def test_patch(
    api_client: TestClient,
    auth_token: tuple[User, dict[str, str]],
    username: str,
    email: str,
) -> None:
    """Test successful patch request."""
    token = auth_token[1]
    user = auth_token[0]

    assert not user.username == username
    assert not user.email == email

    response = api_client.patch(
        URL,
        headers={
            "authorization": f'{token["token_type"].capitalize()} {token["access_token"]}',
        },
        json={"username": username, "email": email},
    )

    response.raise_for_status()
    assert response.status_code == 200
    assert response.reason == "OK"
    json_ = response.json()
    assert json_["username"] == username
    assert json_["email"] == email


@pytest.mark.parametrize("username", ["test-name", "123456"])
def test_patch_409(
    api_client: TestClient,
    auth_token: tuple[User, dict[str, str]],
    username: str,
) -> None:
    """Test failing patch request with a database conflict error."""
    from image_secrets.backend.database.user.models import User

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        User.create(username=username, email="email@email.com", password_hash="pwd"),
    )

    token = auth_token[1]

    response = api_client.patch(
        URL,
        headers={
            "authorization": f'{token["token_type"].capitalize()} {token["access_token"]}',
        },
        json={"username": username},
    )

    assert response.status_code == 409
    assert response.reason == "Conflict"
    json_ = response.json()
    assert json_["detail"] == "account detail already exists"
    assert json_["field"] == "UNIQUE constraint failed"
    assert json_["value"].lstrip() == "user.username"


@pytest.mark.parametrize("username", ["", "00000", "1" * 129])
def test_patch_422_username(
    api_client: TestClient,
    auth_token: tuple[User, dict[str, str]],
    username: str,
) -> None:
    """Test a failing patch request with an invalid username in the body."""
    token = auth_token[1]

    response = api_client.patch(
        URL,
        headers={
            "authorization": f'{token["token_type"].capitalize()} {token["access_token"]}',
        },
        json={"username": username},
    )

    assert response.status_code == 422
    assert response.reason == "Unprocessable Entity"
    assert response.json() == {
        "detail": f"ensure this value has at {'least 6 characters' if len(username) < 6 else 'most 128 characters'}",
        "field": "username",
    }


@pytest.mark.parametrize(
    "email",
    ["", "@", "email@email", "email.com", "email@email.", "@email.com"],
)
def test_patch_422_email(
    api_client: TestClient,
    auth_token: tuple[User, dict[str, str]],
    email: str,
) -> None:
    """Test a failing patch request with an invalid email in the body."""
    token = auth_token[1]

    response = api_client.patch(
        URL,
        headers={
            "authorization": f'{token["token_type"].capitalize()} {token["access_token"]}',
        },
        json={"email": email},
    )

    assert response.status_code == 422
    assert response.reason == "Unprocessable Entity"
    assert response.json() == {
        "detail": "value is not a valid email address",
        "field": "email",
    }


def test_delete(
    api_client: TestClient,
    auth_token: tuple[User, dict[str, str]],
) -> None:
    """Test a successful delete request."""
    token = auth_token[1]
    response = api_client.delete(
        URL,
        headers={
            "authorization": f'{token["token_type"].capitalize()} {token["access_token"]}',
        },
    )

    response.raise_for_status()
    assert response.status_code == 204
    assert response.reason == "No Content"
    with pytest.raises(JSONDecodeError):
        response.json()
    assert not response.headers
