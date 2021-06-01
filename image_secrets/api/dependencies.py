"""API dependencies."""
from __future__ import annotations

import functools as fn
from typing import TYPE_CHECKING

from fastapi_mail import FastMail

from image_secrets.api import config

if TYPE_CHECKING:
    from image_secrets.api.config import Settings


@fn.cache
def get_config() -> Settings:
    """Return api settings."""
    return config.settings


@fn.cache
def get_mail() -> FastMail:
    """Return SMTP mail client."""
    return FastMail(config.email_config)


__all__ = [
    "get_config",
]
