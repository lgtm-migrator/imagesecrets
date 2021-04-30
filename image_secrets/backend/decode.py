"""Module with functions to decode text from images."""
from __future__ import annotations

from pathlib import Path

from image_secrets.backend import util
from image_secrets.backend.settings import MESSAGE_DELIMETER


def decode_text(file: Path) -> str:
    _, arr = util.image_data(file)

    message = ""
    for data in arr.reshape(-1, 8):
        if message[-len(MESSAGE_DELIMETER) :] == MESSAGE_DELIMETER:
            return message

        binary = "".join(map(lambda x: bin(x)[-1], data))
        message += util.binary_to_char(binary)
    else:
        raise StopIteration(f"No message found in {file!s}")


def main(file: Path) -> str:
    """Main decoding function.

    :param file: The Path to the source file

    """
    text = decode_text(file.absolute())
    return text[: -len(MESSAGE_DELIMETER)]
