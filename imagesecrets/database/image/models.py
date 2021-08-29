"""Image database models."""
from imagesecrets.constants import MESSAGE_DELIMITER
from imagesecrets.database.base import Base
from sqlalchemy import Column, ForeignKey, Integer, SmallInteger, String


class Image:
    """Base image mixin."""

    image_name = Column(String)

    message = Column(String)
    delimiter = Column(String, default=MESSAGE_DELIMITER)
    lsb_amount = Column(SmallInteger, default=1)


class DecodedImage(Image, Base):
    """Decoded image model."""

    user_id = Column(Integer, ForeignKey("user.id"))


class EncodedImage(Image, Base):
    """Tortoise encoded image model."""

    user_id = Column(Integer, ForeignKey("user.id"))


__all__ = [
    "Image",
    "DecodedImage",
    "EncodedImage",
]
