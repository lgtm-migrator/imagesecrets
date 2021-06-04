"""Test the CRUD module for token."""
from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

import pytest
from tortoise.exceptions import DoesNotExist

from image_secrets.backend.database.token import crud

if TYPE_CHECKING:
    from pytest_mock import MockFixture

    from image_secrets.backend.database.token.models import Token


@pytest.fixture()
def insert_token(insert_user) -> Token:
    """Return an existing ``Token`` in database."""
    from image_secrets.backend.database.token.models import Token

    token = Token(
        token_hash="test_token_hash",
        owner_id=insert_user.id,
    )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(token.save())

    return token


@pytest.fixture()
def token() -> Token:
    """Return an encoded image."""
    from image_secrets.backend.database.token import models

    t = models.Token(
        token_hash="test_token",
        owner_id=2,
    )
    return t


@pytest.fixture()
def mock_create_token(mocker: MockFixture, token: Token):
    """Return mocked Token.create function."""
    async_mock = mocker.AsyncMock(return_value=token)
    return mocker.patch(
        "image_secrets.backend.database.token.models.Token.create",
        side_effect=async_mock,
    )


@pytest.mark.asyncio
async def test_create(mocker: MockFixture, mock_create_token, token: Token) -> None:
    """Test the create function."""
    token_return = "test_token"
    url_safe = mocker.patch(
        "secrets.token_urlsafe",
        return_value=token_return,
    )
    hash_return = "test_hash"
    hash_ = mocker.patch(
        "image_secrets.backend.password.hash_",
        return_value=hash_return,
    )

    result = await crud.create(0)

    url_safe.assert_called_once_with()
    hash_.assert_called_once_with(token_return)
    token.token_hash = hash_return
    assert result == token_return


@pytest.mark.asyncio
async def test_get_owner_id_ok(mocker: MockFixture, insert_token: Token) -> None:
    """Test successful get_owner_id function call."""
    auth = mocker.patch("image_secrets.backend.password.auth", return_value=True)

    token = "test_token"
    result = await crud.get_owner_id(token)

    auth.assert_called_once_with(token, insert_token.token_hash)
    assert result == insert_token.owner_id


@pytest.mark.asyncio
async def test_get_owner_id_fail(mocker: MockFixture, insert_token: Token) -> None:
    """Test failing get_owner_id function call."""
    auth = mocker.patch("image_secrets.backend.password.auth", return_value=False)

    token = "test_token"

    with pytest.raises(DoesNotExist):
        await crud.get_owner_id(token)
    auth.assert_called_once_with(token, insert_token.token_hash)
