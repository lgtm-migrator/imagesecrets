"""User database models."""
from imagesecrets.database.base import Base
from sqlalchemy import CheckConstraint, Column, String
from sqlalchemy.orm import relationship, validates


class User(Base):
    """User model."""

    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password_hash = Column(String(128))

    decoded_images = relationship("DecodedImage")
    encoded_images = relationship("EncodedImage")

    __table_args__ = (
        CheckConstraint(
            "char_length(username) >= 6",
            name="username_min_length",
        ),
        CheckConstraint(
            "char_length(username) <= 128",
            name="username_max_length",
        ),
    )

    @validates("username")
    def validate_username(self, key, username) -> str:
        """Validate the username column."""
        if not 6 <= len(username) <= 128:
            raise ValueError("Invalid username length.")
        return username
