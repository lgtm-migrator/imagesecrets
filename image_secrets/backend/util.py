"""Utility functions."""
from __future__ import annotations

import itertools as it
from pathlib import Path
from typing import TYPE_CHECKING, Iterable, Iterator, TypeVar

import more_itertools as more_it
import numpy as np
from PIL import Image

if TYPE_CHECKING:
    from numpy.typing import ArrayLike


_T = TypeVar("_T")


def str_to_binary(str_: str, /) -> Iterator[str]:
    """Turn a string into it's binary representation.

    :param str_: The string to convert

    """
    yield from (format(ord(char), "08b") for char in str_)


def split_iterable(it_: Iterable[_T], n: int, /) -> Iterator[list[_T]]:
    """Split an Iterable every nth element.

    :param it_: The iterable to split
    :param n: When to split

    """
    yield from more_it.chunked(it_, n)


def flat_iterable(it_: Iterable[Iterable[_T]], /) -> Iterator[_T]:
    """Flatten the given iterable."""
    yield from it.chain.from_iterable(it_)


def image_data(file: Path, /) -> tuple[tuple[int, int, int], ArrayLike]:
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


def encoded_image_name(file: Path, /) -> Path:
    """Return a new filename with 'encoded_' prefix.

    :param file: The filepath to the image

    """
    name = f"encoded_{file.stem}.png"
    return Path(file.parent, name)
