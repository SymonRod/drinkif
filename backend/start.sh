#!/bin/sh

cd /backend/drinkif/

python3 manage.py migrate

echo "Starting Gunicorn..."
gunicorn --bind 0.0.0.0:8000 drinkif.wsgi 