"""Module with functions to decode text from images."""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np

from image_secrets.backend import util
from image_secrets.settings import MESSAGE_DELIMETER

if TYPE_CHECKING:
    from numpy.typing import DTypeLike


def decode_text(array: DTypeLike) -> str:
    """Decode text.

    :param array: The array which should contain the message

    :raises StopIteration: If the whole array has been checked and nothing was found

    """
    # note: Iterating over the array seems to be faster than running the packbits function
    # on all the elements right away. Probably because image data is huge (fullhd: 6MM+).
    # In the for loop we can return the message early.
    message = ""
    for data in array.reshape(-1, 8):
        if message[-len(MESSAGE_DELIMETER) :] == MESSAGE_DELIMETER:
            return message[: -len(MESSAGE_DELIMETER)]

        # turn the 8 least significant bits in the current array to an integer
        num = np.packbits(np.bitwise_and(data, 0b1))[0]
        message += chr(num)
    else:
        raise StopIteration(f"No message found after scanning the whole image.")


def main(file: str) -> str:
    """Main decoding function.

    :param file: The Path to the source file

    """
    file = Path(file.strip()).absolute()
    _, arr = util.image_data(file)
    text = decode_text(arr)
    return text
