"""Module with pydantic schemas."""
from pydantic import BaseModel


class DecodeSchema(BaseModel):
    """Response model for information about decoding."""

    filename: str
    delimiter: str
    least_significant_bits: int
    reverse_decoding: bool

    def header_dict(self) -> dict:
        """Return a dictionary to be shown in api headers."""
        return {
            key.replace("_", "-"): repr(value)  # bool and int are not hashable
            for key, value in self
        }


class EncodeSchema(DecodeSchema):
    """Response model for information about encoding."""

    message: str
