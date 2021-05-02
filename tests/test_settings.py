"""Test the settings module."""
from image_secrets.settings import MESSAGE_DELIMETER


def test_delimeter():
    """Test that the delimiter is divisible by 3 without any remainder."""
    assert len(MESSAGE_DELIMETER) % 3 == 0
