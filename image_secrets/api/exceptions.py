"""Custom exceptions."""
from fastapi import HTTPException, status

from image_secrets.backend.util.main import partial_init

UnsupportedMediaType = partial_init(
    HTTPException,
    status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    detail="only .png images are supported",
)


class DetailExists(HTTPException):
    """Raised when user tries to claim an account detail which already exists."""

    def __init__(self, status_code: int, message: str, field: str, value: str) -> None:
        """Construct the class."""
        self.status_code = status_code
        self.message = message
        self.field = field
        self.value = value


class NotAuthenticated(Exception):
    """Raised a when an user tries to access a protected resource without being authenticated."""

    def __init__(self, status_code: int = status.HTTP_401_UNAUTHORIZED) -> None:
        """Construct the class."""
        self.status_code = status_code