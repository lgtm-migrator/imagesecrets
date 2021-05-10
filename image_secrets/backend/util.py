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


if __name__ == "__main__":
    from timeit import default_timer

    a = np.array([1, 3, 0, 18], dtype=np.uint8)
    secret = b"hello"
    b = ["0", "1"]

    times = []
    for _ in range(100000):
        now = default_timer()

        a[0] |= int("".join(b), 2)

        times.append(default_timer() - now)
    print("format", min(times))

    a = np.array([1, 3, 0, 18], dtype=np.uint8)
    times = []
    for _ in range(100000):
        now = default_timer()

        a[0] = int(format(a[0], "08b")[:-2] + bin(int(*b, 2)), base=2)

        times.append(default_timer() - now)
    print("bitwise", min(times))

    _ = chr(int("".join(format(i, "08b")[-2:] for i in a), base=2))
    _ = chr(np.packbits(np.bitwise_and(a, 0b1))[0])
