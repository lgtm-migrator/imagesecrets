"""FastAPI configuration."""
import os

from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig, config
from pydantic import BaseSettings, DirectoryPath, EmailStr, PostgresDsn

from image_secrets.settings import API_IMAGES, ENV, MESSAGE_DELIMITER, TEMPLATES

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

# monkey patch one of fastapi_mail path validation functions
# because it is broken when application is not run from parent folder
config.validate_path = lambda _: True
email_config = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_PORT=int(os.getenv("MAIL_PORT")),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_TLS=True,
    MAIL_SSL=False,
    MAIL_FROM=EmailStr(os.getenv("MAIL_FROM")),
    TEMPLATE_FOLDER=str(TEMPLATES),
)

__all__ = [
    "Settings",
]
