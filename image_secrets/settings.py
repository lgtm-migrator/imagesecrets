"""Module with settings."""
from pathlib import Path

ICON = Path(__file__).parent / "static/favicon.ico"

MESSAGE_DELIMITER = "<{~stop-here~}>"

API_IMAGES = Path(__file__).parent / "static/images/"
API_IMAGES.mkdir(parents=True, exist_ok=True)

__all__ = [
    "ICON",
    "MESSAGE_DELIMITER",
]
