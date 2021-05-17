"""FastAPI configuration."""
from pathlib import Path

from pydantic import BaseSettings

from image_secrets.settings import API_IMAGES


class Settings(BaseSettings):
    """API Settings."""

    app_name: str = "ImageSecrets"
    image_folder: Path = API_IMAGES

    class Config:
        """Settings configuration."""

        env_file = ".env"
        env_file_encoding = "utf-8"


__all__ = [
    "Settings",
]
