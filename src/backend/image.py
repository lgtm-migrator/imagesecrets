"""Module with image class for decoding and encoding."""
from typing import Optional
from pathlib import Path

from PIL.Image import open


class Image:
    def __init__(self, image_file: Path) -> None:
        self.image = open(image_file)

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}({self.image!r})"

    def encode(self, message) -> Optional[str]:
        pixels = self.image.getdata()
        print(pixels)
        return f"Encoded message {message!r} into {self.image!s}"

    def decode(self) -> str:
        message = "secret message"
        return f"Message decoded from {self.image!s}:\n{message!r}"
