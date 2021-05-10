"""Module with functions to decode text from images."""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Generator

import numpy as np

from image_secrets.backend import util
from image_secrets.settings import MESSAGE_DELIMETER

if TYPE_CHECKING:
    from numpy.typing import ArrayLike


def decode_text(
    array: ArrayLike,
    delimeter: str = MESSAGE_DELIMETER,
    lsb_n: int = 1,
) -> str:
    """Decode text.

    :param array: The array which should contain the message
    :param delimeter: ...
    :param lsb_n: ...

    :raises StopIteration: If the whole array has been checked and nothing was found

    """
    message = ""
    delim_len = len(delimeter)

    for data in array.reshape(-1, 8 // lsb_n):
        if message[-delim_len:] == delimeter:
            return message[:-delim_len]

        # turn the 8 least significant bits in the current array to an integer
        num = np.packbits(np.bitwise_and(data, 0b1))[0]
        message += chr(num)
    else:
        raise StopIteration("No message found after scanning the whole image.")


def main(
    file,
    delimeter: str,
    lsb_n: int,
    reverse: bool,
) -> str:
    """Main decoding function.

    :param file: The Path to the source file

    """
    img = util.read_coroutine(file)
    _, arr = util.image_data(img)

    arr = prepare_array(arr, lsb_n, reverse)

    text = decode_text(arr, delimeter, lsb_n)
    return text


def api():
    ...


def prepare_array(array: ArrayLike, lsb_n: int, reverse: bool) -> ArrayLike:
    shape = (-1, 8)
    if reverse:
        array = np.flip(array)
    arr = np.unpackbits(array).reshape(shape)
    # cut unnecessary bits and pack the rest
    arr = np.packbits(arr[:, -lsb_n:])
    return arr


def delimeter_check(delimeter) -> Generator:
    delim_len = len(delimeter)
    while 1:
        string = yield
        if string[-delim_len:] == delimeter:
            return string[:-delim_len]
        yield False


def decode_text_(array: ArrayLike, delimeter):
    message = ""
    delim_coro = delimeter(delimeter)
    next(delim_coro)

    for num in array:
        if m := delim_coro.send(message):
            return m
        message += chr(num)
    else:
        raise StopIteration("No message found after scanning the whole image.")


__all__ = [
    "decode_text",
    "main",
]
