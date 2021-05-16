"""Module with pydantic models (schemas)."""
from pydantic import BaseModel, EmailStr


class ImageBase(BaseModel):
    """Base image model."""


class Image(ImageBase):
    """Model for reading image information."""

    image_name: str
    message: str
    delimiter: str
    lsb_amount: int
    reversed: bool

    class Config:
        """Config class to setup orm mode."""

        orm_mode = True


class UserBase(BaseModel):
    """Base user model."""

    username: str
    email: EmailStr


class UserCreate(UserBase):
    """Model for new user creation."""

    password: str


class User(UserBase):
    """Model for reading user information."""

    decoded_images: list[Image] = []
    encoded_images: list[Image] = []

    class Config:
        """Config class to setup orm mode."""

        orm_mode = True
