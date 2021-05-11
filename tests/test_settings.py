"""Test the settings module."""
from image_secrets.settings import API_IMAGES, ICON, MESSAGE_DELIMITER


def test_icon() -> None:
    """Test that a icon exists."""
    assert ICON.is_file()


def test_message_delimeter() -> None:
    """Test that the default message_delimiter exists."""
    assert MESSAGE_DELIMITER


def test_api_images() -> None:
    """Test that the Path to api image storage exists."""
    assert API_IMAGES.is_dir()
