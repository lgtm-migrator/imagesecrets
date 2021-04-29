"""Module with functions to decode text from images."""
from __future__ import annotations

from pathlib import Path

from src.backend import util
from src.backend.settings import MESSAGE_DELIMETER


def decode_text(file: Path) -> str:
    _, arr = util.image_data(file)

    message = ""
    for data in arr.reshape(-1, 8):
        if message[-len(MESSAGE_DELIMETER) :] == MESSAGE_DELIMETER:
            return message

        binary = "".join(map(lambda x: bin(x)[-1], data))
        message += util.binary_to_char(binary)
    else:
        raise StopIteration("No message found.")


def main(file: Path) -> str:
    text = decode_text(file)
    return f"Message decoded from {file!s}:\n{text[:-len(MESSAGE_DELIMETER)]!r}"
