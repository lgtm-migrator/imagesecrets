"""Exception handlers for api."""
from __future__ import annotations

from typing import Optional, Any, TYPE_CHECKING

from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from image_secrets.api.exceptions import DetailExists

if TYPE_CHECKING:
    from fastapi import FastAPI


def init(app: FastAPI):
    """Connect exception handlers to app.

    :param app: The current app instance

    """
    # same as decorator syntax
    app.exception_handler(RequestValidationError)(validation_exception_handler)
    app.exception_handler(DetailExists)(http_exception_handler)


async def handler(
    status_code: int,
    message: str,
    field: str,
    headers: Optional[Any] = None,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder({"info": message, "field": field}),
        headers=headers,
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    errors = exc.errors()[0]
    msg = errors["msg"]
    field = errors["loc"][-1]
    return await handler(status_code=422, message=msg, field=field)


async def http_exception_handler(
    request: Request,
    exc: DetailExists,
) -> JSONResponse:
    return await handler(
        status_code=exc.status_code,
        message=exc.message,
        field=exc.field,
    )
