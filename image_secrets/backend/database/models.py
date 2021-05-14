"""Module with database models."""
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, orm

from image_secrets.backend.database.base import Base
from image_secrets.settings import MESSAGE_DELIMITER


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    items = orm.relationship("Item", back_populates="owner")


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    filename = Column(String, unique=True, index=True)
    image_name = Column(String, index=True)
    message = Column(String, index=True)
    delimiter = Column(String, index=True, default=MESSAGE_DELIMITER)
    lsb_amount = Column(Integer, index=True, default=1)
    reversed = Column(Boolean, index=True, default=False)

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = orm.relationship("User", back_populates="items")
