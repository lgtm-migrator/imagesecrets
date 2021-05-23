"""Test the settings module."""
from image_secrets.settings import API_IMAGES, ENV, ICON, MESSAGE_DELIMITER


def test_env() -> None:
    """Test the file with environment variables."""
    assert ENV.is_file()
    assert ENV.stem == ".env"
    assert not ENV.suffix


def test_icon() -> None:
    """Test the application icon."""
    assert ICON.is_file()
    assert ICON.stem == "favicon"
    assert ICON.suffix == ".ico"
    assert ICON.parent.name == "static"


def test_message_delimiter() -> None:
    """Test that the default message_delimiter exists."""
    assert MESSAGE_DELIMITER


def test_api_images() -> None:
    """Test that the Path to api image storage exists."""
    assert API_IMAGES.is_dir()
    assert API_IMAGES.parent.name == "static"
