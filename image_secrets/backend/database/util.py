"""Utility functions connected to database."""
from __future__ import annotations

import contextlib as ctxlib
from typing import TYPE_CHECKING

from sqlalchemy.exc import ResourceClosedError

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def execute(session: AsyncSession, expression):
    result = await session.execute(expression)
    with ctxlib.suppress(ResourceClosedError):
        return result.scalars()
