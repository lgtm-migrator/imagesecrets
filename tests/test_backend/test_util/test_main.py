"""Test the util_main module."""
from __future__ import annotations

import string

import pytest
from tortoise.exceptions import IntegrityError

from image_secrets.backend.util.main import (
    parse_unique_integrity,
    partial_init,
    token_hex,
)


def test_partial_init() -> None:
    """Test the partial init function."""

    class Test:
        def __init__(self, *args, **kwargs) -> None:
            self.args = args
            self.kwargs = kwargs

        def __repr__(self) -> str:
            return f"{self.args!r}, {self.kwargs!r}"

    partial = partial_init(Test, test="test")
    assert partial.__name__ == "Partial"
    assert partial.mro()[1] is Test
    assert partial.__base__ is Test
    assert partial.__module__ == "image_secrets.backend.util.main"

    initialized = partial("test")
    assert initialized.__repr__() == Test("test", test="test").__repr__()
    assert "test" in initialized.args
    assert initialized.kwargs["test"] == "test"


@pytest.mark.parametrize("length", [16, 64, 33, 0, -8, 101])
def test_token_hex(length) -> None:
    """Test the token_hex function."""
    char_set = {i for i in (string.ascii_lowercase + string.digits)}

    token = token_hex(length)

    length = abs(length)

    assert len(token) == length if length % 2 == 0 else length + 1
    assert all(i in char_set for i in token)


def test_parse_unique_integrity() -> None:
    """Test the parse_unique_integrity function."""
    err = IntegrityError("DETAIL  KEY (username)=(123456) already exists.")
    result = parse_unique_integrity(error=err)
    assert result[0] == "username"
    assert result[1] == "123456"


def test_parse_unique_integrity_fail() -> None:
    """Test that the parse_unique_integrity functions raises ValueError if no result found."""
    err = IntegrityError("invalid error")
    with pytest.raises(ValueError):
        parse_unique_integrity(error=err)
