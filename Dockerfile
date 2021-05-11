FROM python:3.9

RUN pip install poetry

WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

EXPOSE 80

COPY . /app/

RUN pytest

CMD ["python", "bin/run_api.py"]
