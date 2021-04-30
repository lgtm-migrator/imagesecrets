"""Test the regex module."""
import re

import pytest

from image_secrets.backend import regex


@pytest.mark.parametrize(
    "file, expected",
    [
        ("pic.png", True),
        ("png.png", True),
        (" image.png", True),
        ("dir/subdir/img.png", True),
        ("    image.png    ", True),
        ("", False),
        (" ", False),
        ("directory/file.py", False),
        ("test/asdf.ng  ", False),
        (__file__, False),
        ("pictures/image .png", False),
    ],
)
def test_png_ext(file: str, expected: bool) -> None:
    """Test that the regex PNG_EXT pattern works as expected.

    :param file: The filepath to be checked by the regex pattern
    :param expected: Whether the check should be True or False

    """
    assert bool(re.fullmatch(regex.PNG_EXT, file)) is expected
