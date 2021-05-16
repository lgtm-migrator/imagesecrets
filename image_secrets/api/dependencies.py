"""API dependencies"""
from __future__ import annotations

import functools as fn
from typing import TYPE_CHECKING

from image_secrets.api import config
from image_secrets.backend.database.base import async_session

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


@fn.cache
def get_settings():
    """Return api settings."""
    return config.Settings()


async def get_session() -> AsyncSession:
    """Return an asynchronous database session."""
    async with async_session() as session:
        yield session


__all__ = [
    "get_settings",
]
