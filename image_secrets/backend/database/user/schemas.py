"""User schemas."""
import functools as fn
from typing import Optional

from pydantic import EmailStr, SecretStr
from tortoise.contrib.pydantic import pydantic_model_creator

from image_secrets.backend.database.image import schemas
from image_secrets.backend.database.user import models

pydantic_model_creator = fn.partial(
    pydantic_model_creator,
    cls=models.User,
    exclude=("id", "password_hash"),
)
_UserBase = pydantic_model_creator(exclude_readonly=True)
_UserFull = pydantic_model_creator(exclude_readonly=False)


class UserBase(_UserBase):
    """Base User schema."""

    # override email type to get pydantic email validation
    email: EmailStr


class UserCreate(UserBase):
    """Create new User schema."""

    password: SecretStr


class UserUpdate(UserBase):
    """Update existing User schema."""

    username: Optional[str]
    email: Optional[EmailStr]


class User(_UserFull):
    """Main User schema."""

    decoded_images: list[schemas.Image] = []
    encoded_images: list[schemas.Image] = []
