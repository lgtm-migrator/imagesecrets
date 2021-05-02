"""Module with compiled regular expressions."""
import re

_png_ext = """
    ^       # beggining
    \s*?    # non-greedy, zero or more whitespace chars
    \S+     # greedy, anything but whitespace chars
    \.png   # '.png' literally
    \s*     # zero or more whitespace chars
    $       # end
"""
PNG_EXT = re.compile(_png_ext, re.IGNORECASE | re.VERBOSE)

CHARS_8 = re.compile(r"........")


__all__ = [
    "CHARS_8",
    "PNG_EXT",
]
