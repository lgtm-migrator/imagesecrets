"""Utility functions."""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Iterable, Iterator, TypeVar

import more_itertools as more_it
import numpy as np
from PIL import Image

if TYPE_CHECKING:
    from numpy.typing import ArrayLike


T = TypeVar("T")


def str_to_binary(str_: str, /) -> Iterator[str]:
    """Turn a string into it's binary representation.

    :param str_: The string to convert

    """
    yield from ("{0:08b}".format(ord(char), "b") for char in str_)


def split_iterable(it: Iterable, n: int, /) -> Iterator[Iterator[str]]:
    """Split an Iterable every nth element.

    :param it: The iterable to split
    :param n: When to split

    """
    yield from more_it.ichunked(it, n)


def peek_next_elem(it: Iterator[T]) -> T:
    """Return the next element in a given Iterator without advancing it."""
    pk = more_it.peekable(it)
    return pk.peek()


def flat_iterable(it: Iterable) -> Iterable:
    """Flatten the given iterable."""
    return more_it.flatten(it)


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


def encoded_image_name(file: Path) -> Path:
    """Return a new filename with the 'encoded_ prefix'.

    :param file: The filepath to the image

    """
    name = f"encoded_{file.stem}.png"
    return Path(file.parent, name)


if __name__ == "__main__":
    from itertools import islice, repeat, starmap, takewhile, tee

    # operator.truth is *significantly* faster than bool for the case of
    # exactly one positional argument
    from operator import truth
    from timeit import default_timer

    from more_itertools import chunked, ichunked

    def chunker(n, iterable):  # n is size of each chunk; last chunk may be smaller
        return takewhile(
            truth,
            map(tuple, starmap(islice, repeat((iter(iterable), n)))),
        )

    string = "12345678912345678910"
    b_msg = str_to_binary(string + "blabla")

    b_msg = reversed(tuple(b_msg))

    b_msg = "".join(b_msg)

    b_msg1, bmsg2 = tee(split_iterable(b_msg, 1), 2)

    times = []
    for _ in range(1000000):
        now = default_timer()
        _ = more_it.flatten(reversed(string))
        times.append(default_timer() - now)
    print("me", min(times))

    times = []
    for _ in range(1000000):
        now = default_timer()
        _ = "".join(reversed(string))
        times.append(default_timer() - now)
    print("itertools", min(times))
