"""Tasks which should be periodically executed during runtime."""
from __future__ import annotations

import asyncio
import functools as fn
from typing import TYPE_CHECKING, Any, Callable, Coroutine

from pypika import Interval, Parameter

from image_secrets.backend.database.token.models import Token

if TYPE_CHECKING:
    from fastapi import FastAPI


def init(app: FastAPI) -> None:
    """Add startup event to run all tasks.

    :param app: The application which will have the startup event appended

    """

    @app.on_event("startup")
    async def runner() -> None:
        """Run all tasks."""
        await clear_tokens()


_F = Callable[[], Coroutine[Any, Any, None]]


def repeat(*, seconds: int) -> Callable[[_F], _F]:
    """Decorate a coroutine to be run in an infinite loop.

    :param seconds: How often to repeat coroutine call

    """

    def decorator(func: _F) -> _F:
        """Decorate a coroutine.

        :param func: The coroutine to decorate

        """

        @fn.wraps(func)
        async def wrapper() -> None:
            """Wrap the infinite loop execution."""

            async def loop() -> None:
                """Execute decorated function and sleep for the given amount of seconds."""
                while 1:
                    try:
                        await func()
                    except RuntimeError:
                        break
                    await asyncio.sleep(seconds)

            asyncio.ensure_future(loop())

        return wrapper

    return decorator


# since tests are in SQLite, these PostgreSQL specific function can't be tested
# that's the reason for excluding it in coverage report
@repeat(seconds=600)  # 10 minutes
async def clear_tokens() -> None:  # pragma: no cover
    """Clear all expired tokens in database."""
    tokens = Token.filter(
        # query all tokens older than 10 minutes
        created__lte=Parameter("NOW()")
        - Interval(minutes=10),
    )
    await tokens.delete()
