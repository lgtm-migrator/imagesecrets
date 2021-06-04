"""Utility functions."""
from __future__ import annotations

import functools as fn
import math
import re
import secrets
from typing import TYPE_CHECKING

from image_secrets.backend.regex import INTEGRITY_FIELD

if TYPE_CHECKING:
    from typing import Any, Optional, Type

    from tortoise.exceptions import IntegrityError


def partial_init(cls: Type, *args: Optional[Any], **kwargs: Optional[Any]):
    """Partially instantiate a class initializer.

    :param cls: The class to instantiate
    :param args: Optional positional arguments
    :param kwargs: Optional keyword arguments

    """

    class Partial(cls):
        """Partial class with partially initialized initializer."""

        __init__ = fn.partialmethod(cls.__init__, *args, **kwargs)

        # repr with ``Partial`` would be confusing
        __repr__ = cls.__repr__

    return Partial


def token_hex(length: int, /) -> str:
    """Return a random token hex.

    :param length: How many chars should the final token have

    """
    nbytes = math.ceil(abs(length) / 2)
    return secrets.token_hex(nbytes)


def token_url() -> str:
    """Return random and URL safe token."""
    return secrets.token_urlsafe()


# pytest is buggy with this function, todo
def parse_unique_integrity(
    *, error: IntegrityError
) -> Optional[tuple[str, str]]:  # pragma: no cover
    """Parse a database uniqueness IntegrityError and return the conflicting field and value."""
    err = str(error)
    try:
        return re.findall(INTEGRITY_FIELD, err)[0]
    except IndexError as e:
        raise ValueError(f"invalid error message: {err!r}") from e


__all__ = [
    "token_hex",
]
