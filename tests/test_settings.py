"""Test the settings module."""
from image_secrets.settings import API_IMAGES, ICON


def test_constants():
    """Test that the Path constants in settings actually exist."""
    assert API_IMAGES.is_dir()
    assert ICON.is_file()


__all__ = [
    "test_constants",
]
