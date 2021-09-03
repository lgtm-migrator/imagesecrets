"""User schemas."""
from typing import Optional

from imagesecrets.schemas.image import Image
from pydantic import BaseModel, EmailStr, Field, SecretStr, constr


class _BaseUser(BaseModel):
    """Base User schema."""

    username: constr(min_length=6, max_length=128)
    email: EmailStr


class UserCreate(_BaseUser):
    """Schema for User creation."""

    password: SecretStr = Field(..., min_length=6)


class UserUpdate(BaseModel):
    """Schema for User update."""

    username: Optional[str] = Field(
        None,
        min_length=6,
        max_length=6,
    )
    email: Optional[EmailStr]


class User(_BaseUser):
    """Full User schema."""

    decoded_images: list[Image]
    encoded_images: list[Image]
