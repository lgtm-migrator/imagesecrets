"""API endpoint response examples."""
from image_secrets.api.schemas import Conflict, Field, Message

AUTHORIZATION = {401: {"model": Message, "description": "Authorization Error"}}
FORBIDDEN = {403: {"model": Message, "description": "Authorization Error"}}
CONFLICT = {409: {"model": Conflict, "description": "Conflict Error"}}
MEDIA = {415: {"model": Message, "description": "Unsupported Media Type"}}
VALIDATION = {422: {"model": Field, "description": "Validation Error"}}

MESSAGE_NOT_FOUND = {200: {"model": Message, "description": "Nothing Decoded"}}
IMAGE_TOO_SMALL = {422: {"model": Message, "description": "Invalid Image File"}}
