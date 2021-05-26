"""Test the password utility module."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from image_secrets.backend.util.password import auth, hash_

if TYPE_CHECKING:
    from pytest_mock import MockFixture


@pytest.mark.parametrize("password", ["", "321", "my-password"])
def test_hash_(password: str) -> None:
    """Test the hash function."""
    result = hash_(password)

    assert isinstance(result, str)
    assert result[:4] == "$2b$"
    assert len(result) == 60
    assert result.isascii()


def test_auth(mocker: MockFixture) -> None:
    """Test the auth function."""
    checkpw = mocker.patch("bcrypt.checkpw", return_value=True)

    result = auth("plain", "hashed")

    checkpw.assert_called_once_with("plain".encode(), "hashed".encode())
    assert result
