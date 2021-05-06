"""Module with settings."""
from pathlib import Path

ICON = Path(__file__).parent / "static/favicon.ico"

# must be divisible by 3 without any reminder
MESSAGE_DELIMETER = "<{~stop_here~}>"


__all__ = [
    "ICON",
    "MESSAGE_DELIMETER",
]
