"""Module with image class for decoding and encoding."""
from typing import Optional
from pathlib import Path

import PIL.Image as pil_image


def encode_text(file: str, message: str) -> Optional[str]:
    return f"\nEncoded message {message!r} into {file!s}"


def decode_text(file: str) -> str:
    text = "secret message"
    return f"\nMessage decoded from {file!s}:\n{text!r}"
