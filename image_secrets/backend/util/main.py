"""Utility functions."""
from __future__ import annotations

import math
import re
import secrets

from image_secrets.backend.regex import INTEGRITY_FIELD


def token_hex(length: int, /) -> str:
    """Return a random token hex.

    :param length: How many chars should the final token have

    """
    return secrets.token_hex(math.ceil(abs(length) / 2))


def parse_integrity(*, error_message: str) -> tuple[str, str]:
    return re.findall(INTEGRITY_FIELD, error_message)[0]


__all__ = [
    "token_hex",
]
