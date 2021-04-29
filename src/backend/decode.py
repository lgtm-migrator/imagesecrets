"""Module with functions to decode text from images."""
from pathlib import Path

from src.backend.util import image_array


def decode_text(file: Path) -> str:
    ...


def main(file: Path) -> str:
    text = decode_text(file)
    return f"\nMessage decoded from {file!s}:\n{text!r}"
