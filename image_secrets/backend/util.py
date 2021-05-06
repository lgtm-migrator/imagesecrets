"""Utility functions."""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Iterator, Sequence

import numpy as np
from PIL import Image

if TYPE_CHECKING:
    from numpy.typing import ArrayLike


def str_to_binary(string: str, /) -> Iterator[str]:
    """Turn a string into it's binary representation.

    :param string: The string to convert

    """
    yield from map(
        lambda char: format(char, "08b"),
        bytearray(string, encoding="utf-8"),
    )


def split_seq(seq: Sequence, n: int, /) -> Iterator[str]:
    """Split an Iterator every nth element.

    :param seq: The sequence to split
    :param n: When to split

    """
    yield from (seq[i : i + n] for i in range(0, len(seq), n))


def image_data(file: Path) -> tuple[tuple[int, int, int], ArrayLike]:
    """Return numpy array of the given image.

    :param file: The path to the image from which to extract the data

    """
    with Image.open(file).convert("RGB") as img:
        arr = np.asarray(img, dtype=np.uint8)
    return arr.shape, arr


def save_image(arr: ArrayLike, filepath: Path) -> None:
    """Save a new image.

    :param arr: The numpy array with the pixel data
    :param filepath: The path where the image should be saved

    """
    Image.fromarray(np.uint8(arr)).convert("RGB").save(filepath)


def reverse_data(msg: str, array: ArrayLike) -> tuple[Iterator[str], ArrayLike]:
    return reversed(msg), np.flip(array)


def encoded_image_name(file: Path) -> Path:
    """Return a new filename with the 'encoded_ prefix'.

    :param file: The filepath to the image

    """
    name = f"encoded_{file.stem}.png"
    return Path(file.parent, name)
