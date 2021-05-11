"""Module with pydantic schemas."""
from typing import Optional

from pydantic import BaseModel


class DecodeSchema(BaseModel):
    """Response model for information about decoding."""

    message: Optional[str]
    filename: str
    delimiter: str
    least_significant_bits: int
    reverse_decoding: bool
