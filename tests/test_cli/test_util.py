"""Test utility module for CLI."""
import pytest
from click.exceptions import BadParameter

from image_secrets.cli.cli_util import validate_png


@pytest.mark.parametrize(
    "filename",
    [
        "",
        " ",
        "file",
        " file ",
        "file.image",
        "path/dir/image.jpg",
        "X:/abc/png",
    ],
)
def test_validate_png(filename: str) -> None:
    """Test that an exception is raised when a wrong filename is passed."""
    with pytest.raises(BadParameter):
        validate_png(..., filename)


__all__ = [
    "test_validate_png",
]
