"""API dependencies"""
import functools as fn

from image_secrets.api import config


@fn.cache
def get_settings():
    """Return the api settings."""
    return config.Settings()
