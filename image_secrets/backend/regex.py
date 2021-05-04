"""Module with compiled regular expressions."""
import re

_png_ext = """
   ^                # beginning
   \s*?             # lazy whitespaces
   [A-Za-z]:        # Path drive (eg. C: or F:)
   (?:              # start of non-capturing group
   (?:              # start of nested non-capturing group
   \\|/)            # \ or / literally, once
   \w+)+            # any number of chars, zero times or more
   \w+?             # lazy any char
   \.png            # .png literally
   \s*              # any nunmber of whitespace chars
   $                # end
"""
PNG_EXT = re.compile(_png_ext, re.IGNORECASE | re.VERBOSE)

CHARS_8 = re.compile(r"........")  # any 8 characters


__all__ = [
    "CHARS_8",
    "PNG_EXT",
]
