"""Utility functions."""
from __future__ import annotations

import re
from typing import TYPE_CHECKING
from pathlib import Path

import click
import numpy as np
from PIL import Image

from regex import PNG_EXT

if TYPE_CHECKING:
    from numpy.typing import ArrayLike


def image_array(file: Path) -> ArrayLike:
    """Return numpy array of the given image.

    :param file: The path to the image from which to extract the data

    """
    with Image.open(file).convert("RGB") as img:
        return np.asarray(img.getdata(), dtype=np.uint8)


def validate_png(_, file: str):
    """Validate that the file has as png extension.

    :param _: Dump the context passed in by click
    :param file: The file to check

    :raises BadParameter: If the pattern does not match

    """
    if re.match(PNG_EXT, file):
        return file
    raise click.BadParameter(f"The {file!s} is not a .PNG image.")
