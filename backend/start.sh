#!/bin/sh

cd /backend/drinkif/

ls -lah

pwd

python3 manage.py migrate

python3 manage.py collectstatic --noinput

echo "Starting Gunicorn..."
gunicorn drinkif.wsgi 