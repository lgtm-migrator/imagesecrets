"""Module with pydantic schemas."""
from pydantic import BaseModel, EmailStr, constr


class Message(BaseModel):
    """Response model for a single detail field."""

    detail: str


class Field(Message):
    """Response model for invalid field value."""

    field: str


class Conflict(Field):
    """Response model for conflicting field value."""

    value: str


class Token(BaseModel):
    """Response model for access token."""

    access_token: str
    token_type: str


class ChangePassword(BaseModel):
    """Change User password schema."""

    old: str
    new: constr(min_length=6)


class ResetEmail(BaseModel):
    """Schema for requesting a reset password token."""

    email: EmailStr


class ResetPassword(BaseModel):
    """Schema for requesting a new password for an account."""

    password: str
