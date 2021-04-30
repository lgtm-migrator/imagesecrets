"""Utility functions."""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np
from PIL import Image

if TYPE_CHECKING:
    from numpy.typing import DTypeLike


def str_to_binary(string: str) -> str:
    """Turn a string into it's binary representation.

    :param string: The string to convert

    """
    return "".join(
        map(
            lambda char: format(char, "b").zfill(8),
            bytearray(string, encoding="utf-8"),
        ),
    )


def binary_to_char(binary: str) -> str:
    """Turn the given binary string into a character.

    :param binary: The string containing the binary value to be converted

    """
    return chr(int(binary, base=2))


def image_data(file: Path) -> tuple[tuple[int, int, int], DTypeLike]:
    """Return numpy array of the given image.

    :param file: The path to the image from which to extract the data

    """
    with Image.open(file).convert("RGB") as img:
        arr = np.asarray(img, dtype=np.uint8)
    return arr.shape, arr.flatten()
