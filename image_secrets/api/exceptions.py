"""Custom exceptions."""
from typing import Any, Optional

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


class DetailExists(HTTPException):
    def __init__(self, status_code: int, message: str, field: str):
        self.status_code = status_code
        self.message = message
        self.field = field
