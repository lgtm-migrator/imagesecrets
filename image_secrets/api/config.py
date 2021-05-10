"""FastAPI configuration."""
from pathlib import Path

from pydantic import BaseSettings

from image_secrets.settings import API_IMAGES


class Settings(BaseSettings):
    """Settings class."""

    app_name: str = "ImageSecrets"
    image_folder: Path = API_IMAGES
