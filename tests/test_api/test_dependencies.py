def test_get_config():
    from imagesecrets.api import dependencies
    from imagesecrets.config import settings

    config = dependencies.get_config()

    assert config is settings
