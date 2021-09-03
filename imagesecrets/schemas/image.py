"""Image schemas."""
from __future__ import annotations

from datetime import datetime

from imagesecrets.constants import MESSAGE_DELIMITER
from pydantic import BaseModel, conint


class _ImageBase(BaseModel):
    """Base image schema."""

    image_name: str


class ImageCreate(_ImageBase):
    """Create image schema."""

    message: str
    delimiter: str = MESSAGE_DELIMITER
    lsb_amount: conint(ge=1, le=8) = 1

    filename: str


class ImageUpdate(_ImageBase):
    """Update image schema."""


class Image(ImageCreate):
    """Main Image schema."""

    created: datetime
    modified: datetime
