"""Module with settings."""
from pathlib import Path

ENV = Path(__file__).parent.parent / ".env"
ICON = Path(__file__).parent / "static/favicon.ico"

MESSAGE_DELIMITER = "<{~stop-here~}>"

API_IMAGES = Path(__file__).parent / "static/images"
API_IMAGES.mkdir(parents=True, exist_ok=True)
