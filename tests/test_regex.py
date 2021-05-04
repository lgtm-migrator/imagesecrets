"""Test the regex module."""
import re

import pytest

from image_secrets.backend import regex


@pytest.mark.parametrize(
    "file",
    [
        "pic.png",
        "png.png",
        " image.png",
        "dir/subdir/img.png",
        "    image.png    ",
        "",
        __file__,
        "C:pic.png",
        "F:/directory/file.py",
        "F:\\directory/file.py",
        "pictures/image .png",
    ],
)
def test_png_ext(file: str) -> None:
    """Test that the regex PNG_EXT pattern works as expected.

    :param file: The filepath to be checked by the regex pattern

    """
    assert not re.fullmatch(regex.PNG_EXT, file)


__all__ = [
    "test_png_ext",
]
