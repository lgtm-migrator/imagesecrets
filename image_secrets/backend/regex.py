"""Module with compiler regular expressions."""
import re

# greedy check that string ends with '.png'
PNG_EXT = re.compile(r"^.*\.png$", re.IGNORECASE)
