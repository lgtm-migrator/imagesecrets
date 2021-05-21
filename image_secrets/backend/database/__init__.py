"""Package with everything connected to database."""
from tortoise import Tortoise

from image_secrets.backend.database.image import models as image_models
from image_secrets.backend.database.user import models as user_models

# models are initialized early so we can create correct pydantic schemas
Tortoise.init_models(models_paths=(image_models, user_models), app_label="models")
