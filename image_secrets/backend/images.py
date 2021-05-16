"""Module with CRUD operations connected to images."""
from typing import TYPE_CHECKING, Union

from sqlalchemy.orm import Session

from image_secrets.backend.database import models, schemas

if TYPE_CHECKING:
    from image_secrets.backend.database.schemas import ImageCreate


def get(db: Session, image_model: models.Image, user_id: int):
    """Return all images associated with a user.

    :param db: Database Session
    :param image_model: Model of the wanted image(s)
    :param user_id: Database id of the image owner

    """
    return db.query(image_model).filter(models.User.id == user_id).all()


def create(db: Session, image: ImageCreate, user_id: int):
    """Create a new image in the database.

    :param db: Database Session
    :param image_model: Model of the wanted image(s)
    :param user_id: Database id of the image owner

    """
    db_item = models.Image(**image.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
