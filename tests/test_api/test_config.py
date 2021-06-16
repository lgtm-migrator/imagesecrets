"""Test API configuration."""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from image_secrets.api.config import config as lib_config
from image_secrets.api.config import settings

if TYPE_CHECKING:
    from image_secrets.api.config import Settings


@pytest.fixture(scope="module")
def api_settings() -> Settings:
    """Return API settings."""
    return settings


def test_validate_path_patch() -> None:
    """Test that the library function was successfully monkey patched."""
    assert lib_config.validate_path(...)


def test_attributes(api_settings: Settings) -> None:
    """Test the settings attributes."""
    assert settings.app_name == "ImageSecrets"
    assert settings.message_delimiter
    assert isinstance(settings.image_folder, Path)


def test_email_config(api_settings: Settings) -> None:
    """Test the email_config method."""
    assert api_settings.email_config()
