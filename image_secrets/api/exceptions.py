"""API exceptions."""
from typing import Any, Optional

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


class DetailExists(HTTPException):
    def __init__(self, status_code: int, message: str, field: str):
        self.status_code = status_code
        self.message = message
        self.field = field


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
