#!/bin/bash

echo "creating environment and installing dependencies for ImageSecrets."

python --version

echo "installing poetry"
python -m pip install poetry

echo "installing dependencies from pyproject.toml"
poetry --version
poetry install --no-interaction --no-ansi
