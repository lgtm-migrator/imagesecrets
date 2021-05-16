"""Module with pydantic schemas."""
from pydantic import BaseModel


class DecodeSchema(BaseModel):
    """Response model for information about decoding."""

    filename: str
    custom_delimiter: str
    least_significant_bit_amount: int
    reversed_encoding: bool

    def header_dict(self) -> dict:
        """Return a dictionary to be shown in api headers."""
        return {key.replace("_", "-"): repr(value) for key, value in self}


class EncodeSchema(DecodeSchema):
    """Response model for information about encoding."""

    message: str


class Token(BaseModel):
    """Response model for access token."""

    access_token: str
    token_type: str
