"""Module with compiled regular expressions."""
import re

CHARS_8 = re.compile(r"........")  # any 8 characters


__all__ = [
    "CHARS_8",
]
