"""User schemas."""
import functools as fn
from typing import Optional

from pydantic import EmailStr, Field, SecretStr
from tortoise.contrib.pydantic import pydantic_model_creator

from image_secrets.backend.database.image import schemas
from image_secrets.backend.database.user import models
from image_secrets.backend.regex import USERNAME

USERNAME = USERNAME.pattern
pydantic_model_creator = fn.partial(
    pydantic_model_creator,
    cls=models.User,
    exclude=("id", "password_hash"),
)
_UserBase = pydantic_model_creator(name="UserBase", exclude_readonly=True)
_UserFull = pydantic_model_creator(name="User", exclude_readonly=False)


class UserBase(_UserBase):
    """Base User schema."""

    username: str = Field(..., min_length=6, max_length=128, regex=USERNAME)
    email: EmailStr


class UserCreate(UserBase):
    """Create new User schema."""

    password: SecretStr


class UserUpdate(UserBase):
    """Update existing User schema."""

    username: Optional[str] = Field(None, min_length=6, max_length=128, regex=USERNAME)
    email: Optional[EmailStr]


class User(_UserFull):
    """Main User schema."""

    decoded_images: list[schemas.Image]
    encoded_images: list[schemas.Image]
