"""Image database models."""
from __future__ import annotations

from imagesecrets.constants import MESSAGE_DELIMITER
from imagesecrets.database.base import Base
from sqlalchemy import Column, ForeignKey, Integer, SmallInteger, String
from sqlalchemy.orm import relationship


class Image:
    """Base image mixin."""

    image_name = Column(String)

    message = Column(String)
    delimiter = Column(String, default=MESSAGE_DELIMITER)
    lsb_amount = Column(SmallInteger, default=1)


class DecodedImage(Image, Base):
    """Decoded image model."""

    user_id = Column(Integer, ForeignKey("user.id"))

    parent = relationship("User", back_populates="decodedimage")


class EncodedImage(Image, Base):
    """Encoded image model."""

    user_id = Column(Integer, ForeignKey("user.id"))

    parent = relationship("User", back_populates="encodedimage")


__all__ = [
    "Image",
    "DecodedImage",
    "EncodedImage",
]
