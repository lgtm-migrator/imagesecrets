"""Test the settings module."""
from src.backend.settings import MESSAGE_DELIMETER


def test_delimeter():
    """Test that the specified delimiter is divisible by 3 without any remainder."""
    assert len(MESSAGE_DELIMETER) % 3 == 0
