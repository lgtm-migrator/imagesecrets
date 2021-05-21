"""Image schemas."""
import functools as fn
from datetime import datetime

from pydantic import BaseModel, SecretStr
from tortoise.contrib.pydantic import pydantic_model_creator

from image_secrets.backend.database.image import models

pydantic_model_creator = fn.partial(
    pydantic_model_creator,
    # decoded and encoded are interchangeable as a blueprint for schema
    cls=models.DecodedImage,
    name="ImageBase",
    exclude=("id", "filename", "image_name", "message"),
)
_ImageBase = pydantic_model_creator(exclude_readonly=False)


class DecodeImageCreate(_ImageBase):
    """Create decode image schema."""


class EncodeImageCreate(_ImageBase):
    """Create encode image schema."""

    message: SecretStr


class ImageUpdate(BaseModel):
    """Update image schema."""

    image_name: str


class Image(_ImageBase):
    """Main Image schema."""

    message: SecretStr
    image_name: str

    created: datetime
    modified: datetime
