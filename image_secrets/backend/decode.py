"""Module with functions to decode text from images."""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

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


def main(file: str) -> str:
    """Main decoding function.

    :param file: The Path to the source file

    """
    file = Path(file.strip()).absolute()
    _, arr = util.image_data(file)
    text = decode_text(arr)
    return text


__all__ = [
    "decode_text",
    "main",
]
