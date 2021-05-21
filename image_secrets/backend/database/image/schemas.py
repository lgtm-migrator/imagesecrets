"""Image schemas."""
from datetime import datetime

from devtools import debug
from pydantic import BaseModel, Field
from tortoise.contrib.pydantic import pydantic_model_creator

from image_secrets.backend.database.image import models
from image_secrets.backend.regex import PNG

_ImageBase = pydantic_model_creator(
    cls=models.DecodedImage,
    name="ImageBase",
    exclude=("id", "filename", "owner"),
    exclude_readonly=True,
)


class ImageCreate(_ImageBase):
    """Create image schema."""

    image_name: str = Field(..., max_length=128, regex=PNG.pattern)
    filename: str


class ImageUpdate(BaseModel):
    """Update image schema."""

    image_name: str


class Image(_ImageBase):
    """Main Image schema."""

    created: datetime
    modified: datetime
