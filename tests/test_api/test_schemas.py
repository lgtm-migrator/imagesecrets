"""Test API response schemas."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from image_secrets import settings


@pytest.mark.parametrize(
    "key, result",
    [
        ("", ""),
        ("a", "A"),
        ("A", "A"),
        ("testkey", "TestKey"),
        ("camel", "Camel"),
        ("camel_case", "CamelCase"),
    ],
)
def test_pretty_key(key: str, result: str) -> None:
    """Test the pretty_key function."""
    settings.URL_KEY_ALIAS = {"testkey": "TestKey"}
