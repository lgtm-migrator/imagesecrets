"""Module with pydantic schemas."""
from pydantic import BaseModel


class DecodeSchema(BaseModel):
    """Response model for information about decoding."""

    filename: str
    delimiter: str
    least_significant_bits: int
    reverse_decoding: bool
