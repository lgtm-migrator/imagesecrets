"""Test the util_main module."""
from __future__ import annotations

import string

import pytest

from image_secrets.backend.util import main


@pytest.mark.parametrize("length", [16, 64, 33, 0, -8, 101])
def test_token_hex(length) -> None:
    """Test the token_hex function."""
    char_set = {i for i in (string.ascii_lowercase + string.digits)}

    token = main.token_hex(length)

    length = abs(length)

    assert len(token) == length if length % 2 == 0 else length + 1
    assert all(i in char_set for i in token)
