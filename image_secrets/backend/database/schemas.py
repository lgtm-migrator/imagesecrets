"""Module with pydantic models (schemas)."""
from pydantic import BaseModel


class ImageBase(BaseModel):
    """Base image model."""

    delimiter: str
    lsb_amount: int
    reversed: bool


class DecodeImageCreate(ImageBase):
    """Model for new image creation via decoding data from it."""


class EncodeImageCreate(ImageBase):
    """Model for new image creation via encoding data from it."""

    message: str


class Image(ImageBase):
    """Model for reading image information."""

    id: int
    filename: str
    image_name: str
    message: str

    owner_id: int

    class Config:
        """Config class to setup orm mode."""

        orm_mode = True


class UserBase(BaseModel):
    """Base user model."""

    username: str
    email: str


class UserCreate(UserBase):
    """Model for new user creation."""

    password: str


class User(UserBase):
    """Model for reading user information."""

    id: int
    items: list[Image] = []

    class Config:
        """Config class to setup orm mode."""

        orm_mode = True
