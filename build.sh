#!/usr/bin/env bash
# exit on error
set -o errexit

# Install required modules
pip install -r requirements.txt

# Compile static user stylesheets and canvas vector files
python manage.py collectstatic --no-input

# Run production database migration rows safely
python manage.py migrate