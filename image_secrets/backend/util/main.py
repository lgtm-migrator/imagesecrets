"""Utility functions."""
from __future__ import annotations

import functools as fn
import math
import re
import secrets
from typing import TYPE_CHECKING, Any, Optional, Type

from image_secrets.backend.regex import INTEGRITY_FIELD

if TYPE_CHECKING:
    from tortoise.exceptions import IntegrityError


def partial_init(cls: Type, *args: Optional[Any], **kwargs: Optional[Any]):
    """Partially instantiate a class initializer.

    :param cls: The class to instantiate
    :param args: Optional positional arguments
    :param kwargs: Optional keyword arguments

    """

    class Partial(cls):
        """Partial class with partially initialized __init__."""

        __init__ = fn.partialmethod(cls.__init__, *args, **kwargs)

        # repr with Partial would be confusing
        def __repr__(self) -> str:
            """Provide information about the parent class."""
            return f"Partial class of {cls.__qualname__!r} in {cls.__module__!r}"

    return Partial


def token_hex(length: int, /) -> str:
    """Return a random token hex.

    :param length: How many chars should the final token have

    """
    return secrets.token_hex(math.ceil(abs(length) / 2))


def parse_integrity(*, error_message: IntegrityError) -> tuple[str, str]:
    """Parse a database IntegrityError and return the conflicting field and value."""
    return re.findall(INTEGRITY_FIELD, str(error_message))[0]


__all__ = [
    "token_hex",
]
