"""Base schemas."""
from __future__ import annotations

from pydantic import BaseModel


class ModelSchema(BaseModel):
    """Base schema for database models."""

    class Config:
        """Pydantic configuration."""

        orm_mode = True
