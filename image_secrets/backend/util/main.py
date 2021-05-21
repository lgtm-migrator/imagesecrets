"""Utility functions."""
from __future__ import annotations

import math
import re
import secrets
from typing import TYPE_CHECKING

from image_secrets.backend.regex import INTEGRITY_FIELD

if TYPE_CHECKING:
    from tortoise.exceptions import IntegrityError


def token_hex(length: int, /) -> str:
    """Return a random token hex.

    :param length: How many chars should the final token have

    """
    return secrets.token_hex(math.ceil(abs(length) / 2))


def parse_integrity(*, error_message: IntegrityError) -> tuple[str, str]:
    return re.findall(INTEGRITY_FIELD, str(error_message))[0]


__all__ = [
    "token_hex",
]
