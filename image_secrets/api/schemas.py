"""Module with pydantic schemas."""
from typing import Any, Optional

from pydantic import BaseModel


class Decode(BaseModel):
    """Response model for information about decoding."""

    filename: str
    custom_delimiter: str
    least_significant_bit_amount: int
    reversed_encoding: bool

    def header_dict(self) -> dict:
        """Return a dictionary to be shown in api headers."""
        return {key.replace("_", "-"): repr(value) for key, value in self}


class Encode(Decode):
    """Response model for information about encoding."""

    message: str


class Token(BaseModel):
    """Response model for access token."""

    access_token: str
    token_type: str


class Message(BaseModel):
    """Response model for a single detail field."""

    detail: str


class Field(Message):
    """Response model for invalid field value."""

    field: str


class Conflict(Field):
    """Response model for conflicting field value."""

    value: str
