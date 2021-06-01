"""FastAPI configuration."""
import os

from fastapi_mail import ConnectionConfig, config
from pydantic import BaseSettings, DirectoryPath, EmailStr, PostgresDsn

from image_secrets.settings import API_IMAGES, MESSAGE_DELIMITER, TEMPLATES

# monkey patch one of fastapi_mail path validation functions
# because it is broken when application is not run from parent folder
config.validate_path = lambda _: True


class Settings(BaseSettings):
    """API Settings."""

    app_name: str = "ImageSecrets"

    message_delimiter: str = MESSAGE_DELIMITER
    image_folder: DirectoryPath = API_IMAGES

    pg_dsn: PostgresDsn = os.getenv("DATABASE_URL")
    secret_key: str = os.getenv("SECRET_KEY")

    @staticmethod
    def email_config() -> ConnectionConfig:
        """Return email connection configuration."""
        return ConnectionConfig(
            MAIL_USERNAME=os.getenv("MAIL_USERNAME") or "username",
            MAIL_PASSWORD=os.getenv("MAIL_PASSWORD") or "password",
            MAIL_PORT=int(os.getenv("MAIL_PORT") or 0),
            MAIL_SERVER=os.getenv("MAIL_SERVER") or "server",
            MAIL_TLS=True,
            MAIL_SSL=False,
            MAIL_FROM=EmailStr(os.getenv("MAIL_FROM") or "string@example.com"),
            TEMPLATE_FOLDER=str(TEMPLATES),
        )


settings = Settings()


__all__ = [
    "Settings",
]
