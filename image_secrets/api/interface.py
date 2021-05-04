"""Application Programming Interface"""
from pathlib import Path

from fastapi import FastAPI, File, UploadFile
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse

from image_secrets.backend.decode import decode_text
from image_secrets.backend.encode import encode_message, save_image
from image_secrets.backend.util import image_data, str_to_binary
from image_secrets.settings import MESSAGE_DELIMETER

app = FastAPI()


@app.get("/")
@app.get("/home")
async def home() -> dict:
    """The home route."""
    return {"home": "ImageSecrets Home Page"}


@app.post("/encode")
async def encode(message: str, file: UploadFile = File(...)) -> FileResponse:
    """Encode a message into the source image.

    :param message: Message to encode
    :param file: Source image

    """
    _, arr = image_data(file.file)

    try:
        data = encode_message(
            arr.shape,
            arr,
            str_to_binary(message + MESSAGE_DELIMETER),
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=e.args)

    images = Path(f"images/").absolute()
    images.mkdir(exist_ok=True)
    fp = images / file.filename
    save_image(data, fp)
    return FileResponse(fp)


@app.post("/decode")
async def decode(file: UploadFile = File(...)) -> dict[str:str, str:str]:
    """Decode a message from the given file.

    :param file: The uploaded file

    """
    _, arr = image_data(file.file)

    try:
        return {"file": file.filename, "message": decode_text(arr)}
    except StopIteration as e:
        raise HTTPException(status_code=400, detail=e.args)
