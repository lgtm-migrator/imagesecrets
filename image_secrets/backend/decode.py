"""Module with functions to decode text from images."""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from image_secrets.backend import util
from image_secrets.backend.settings import MESSAGE_DELIMETER

if TYPE_CHECKING:
    from numpy.typing import DTypeLike


def decode_text(array: DTypeLike) -> str:
    """Decode text.

    :param array: The array which should contain the message

    :raises StopIteration: If the whole array has been checked and nothing was found

    """
    message = ""
    for data in array.reshape(-1, 8):
        if message[-len(MESSAGE_DELIMETER) :] == MESSAGE_DELIMETER:
            return message[: -len(MESSAGE_DELIMETER)]

        # join the 8 least significant bits in the current array of pixel data
        binary = "".join((bin(num)[-1] for num in data))
        message += util.binary_to_char(binary)
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
