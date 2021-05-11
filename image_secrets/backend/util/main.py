"""Utility functions."""
from __future__ import annotations

import math
import secrets


def token_hex(length: int, /) -> str:
    """Return a random token hex.

    :param length: How many chars should the final token have

    """
    return secrets.token_hex(math.ceil(abs(length) / 2))


__all__ = [
    "token_hex",
]
