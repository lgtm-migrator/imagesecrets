"""Module with functions to decode text from images."""
from pathlib import Path


def text(file: Path) -> str:
    text = "secret message"
    return f"\nMessage decoded from {file!s}:\n{text!r}"
