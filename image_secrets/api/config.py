"""FastAPI configuration."""
from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Settings class."""

    app_name: str = "ImageSecrets"
    image_folder: Path = Path(f"images/").absolute()
