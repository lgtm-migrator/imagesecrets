"""Custom fields for image models."""
from tortoise.fields import IntField


class LSBIntField(IntField):
    """Custom IntField with overridden constraints for range (1-8)."""

    @property
    def constraints(self) -> dict:
        """Constraints property."""
        return {"ge": 1, "le": 8}
