from fastapi import FastAPI

from imagesecrets import interface


def test_create_application():
    assert isinstance(interface.create_application(), FastAPI)
