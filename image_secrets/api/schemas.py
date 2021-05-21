"""Module with pydantic schemas."""
from pydantic import BaseModel


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
