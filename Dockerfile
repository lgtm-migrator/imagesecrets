FROM python:3.9-slim

MAINTAINER lukas.kucera.g@protonmail.com

RUN pip install poetry

WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

COPY . /app/

RUN pytest

ENTRYPOINT ["python", "bin/run_api.py"]
