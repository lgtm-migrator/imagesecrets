"""Token database model."""
from tortoise import fields, models


class Token(models.Model):
    """Tortoise Token model."""

    id = fields.IntField(pk=True, index=True)
    created = fields.DatetimeField(auto_now_add=True, index=True)

    token = fields.CharField(max_length=128, index=True)

    owner = fields.OneToOneField("models.User", on_delete=fields.CASCADE)

    class Meta:
        """Tortoise metaclass."""

        table = "token"


__models__ = [Token]

__all__ = ["Token"]
