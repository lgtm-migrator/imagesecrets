from fastapi import FastAPI


def test_create_application():
    from imagesecrets import interface

    assert isinstance(interface.create_application(), FastAPI)
