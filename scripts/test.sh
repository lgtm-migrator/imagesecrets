#!/bin/bash

echo "running pytest for image_secrets with coverage"
poetry run pytest --cov=image_secrets
