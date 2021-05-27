"""FastAPI configuration."""
import os

from dotenv import load_dotenv
from pydantic import BaseSettings, DirectoryPath, PostgresDsn

from image_secrets.settings import API_IMAGES, ENV, MESSAGE_DELIMITER

load_dotenv()


class Settings(BaseSettings):
    """API Settings."""

    app_name: str = "ImageSecrets"

    message_delimiter: str = MESSAGE_DELIMITER
    image_folder: DirectoryPath = API_IMAGES

    pg_dsn: PostgresDsn = os.getenv("DATABASE_URL")
    secret_key: str = os.getenv("SECRET_KEY")

    class Config:
        """Settings configuration."""

        env_file = ENV


settings = Settings()


__all__ = [
    "Settings",
]
