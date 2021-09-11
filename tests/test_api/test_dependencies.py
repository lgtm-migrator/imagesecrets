from imagesecrets.api import dependencies
from imagesecrets.config import settings


def test_get_config():
    config = dependencies.get_config()

    assert config is settings
