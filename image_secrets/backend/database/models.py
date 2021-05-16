"""Module with database models."""
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, orm

from image_secrets.backend.database.base import Base, engine
from image_secrets.settings import MESSAGE_DELIMITER


class User(Base):
    """Database model for user."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    decoded_images = orm.relationship("DecodedImage", back_populates="owner")
    encoded_images = orm.relationship("EncodedImage", back_populates="owner")


class ImageMixin:
    """Database user for image."""

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    filename = Column(String, unique=True, index=True)
    image_name = Column(String)
    message = Column(String)
    delimiter = Column(String, default=MESSAGE_DELIMITER)
    lsb_amount = Column(Integer, default=1)
    reversed = Column(Boolean, default=False)


class DecodedImage(ImageMixin, Base):
    """Database model for images in the decoded_images table."""

    __tablename__ = "decoded_images"

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = orm.relationship("User", back_populates="decoded_images")


class EncodedImage(ImageMixin, Base):
    """Database model for images in the encoded_images table."""

    __tablename__ = "encoded_images"

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = orm.relationship("User", back_populates="encoded_images")
