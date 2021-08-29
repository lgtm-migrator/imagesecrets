"""Token database models."""
from imagesecrets.database.base import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import backref, relationship


class Token(Base):
    """Token model."""

    token_hash = Column(String(128))

    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("User", backref=backref("token", uselist=False))


__all__ = ["Token"]
