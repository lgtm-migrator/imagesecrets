"""API dependencies."""
from __future__ import annotations

import functools as fn

from image_secrets.api import config


@fn.cache
def get_config():
    """Return api settings."""
    return config.settings


__all__ = [
    "get_config",
]
