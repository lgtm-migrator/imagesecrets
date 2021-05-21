"""API endpoint response examples."""
from image_secrets.api.schemas import Conflict, Field, Message

AUTHORIZATION = {401: {"model": Message, "description": "Authorization Error"}}
NOT_FOUND = {404: {"model": Message, "description": "Authorization Error"}}
CONFLICT = {409: {"model": Conflict, "description": "Conflict Error"}}
VALIDATION = {422: {"model": Field, "description": "Validation Error"}}
