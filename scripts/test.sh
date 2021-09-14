#!/usr/bin/env bash

SRC="imagesecrets"

poetry run mypy $SRC --verbose
poetry run pytest --verbose --cov=$SRC --cov-report=xml
