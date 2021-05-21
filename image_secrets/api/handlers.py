"""Exception handlers for api."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from image_secrets.api.exceptions import DetailExists, NotAuthenticated

if TYPE_CHECKING:
    from fastapi import FastAPI


def init(app: FastAPI) -> None:
    """Connect exception handlers to app.

    :param app: The current app instance

    """
    # same as decorator syntax
    app.exception_handler(RequestValidationError)(validation_error)
    app.exception_handler(DetailExists)(detail_exists)
    app.exception_handler(NotAuthenticated)(not_authenticated)


async def handler(
    status_code: int,
    message: str,
    field: str,
    value: Optional[str] = None,
    headers: Optional[Any] = None,
) -> JSONResponse:
    content = {"info": message, "field": field}
    if value:
        content |= {"value": value}
    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder(content),
        headers=headers,
    )


async def validation_error(req: Request, exc: RequestValidationError) -> JSONResponse:
    errors = exc.errors()[0]
    msg = errors["msg"]
    field = errors["loc"][-1]
    return await handler(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        message=msg,
        field=field,
    )


async def detail_exists(req: Request, exc: DetailExists) -> JSONResponse:
    return await handler(
        status_code=exc.status_code,
        message=exc.message,
        field=exc.field,
        value=exc.value,
    )


async def not_authenticated(req: Request, exc: NotAuthenticated) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": "invalid access token"},
        headers={"WWW-Authenticate": "Bearer"},
    )
