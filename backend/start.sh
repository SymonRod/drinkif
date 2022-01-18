#!/bin/sh

cd /backend/drinkif/

ls -lah

pwd

python3 manage.py migrate

python3 manage.py collectstatic --noinput

echo "Starting Gunicorn..."
/usr/local/bin/gunicorn -e DJANGO_SETTINGS_MODULE="$APP_NAME".settings "$APP_NAME".wsgi:application -b :8000 -w 2 --timeout 900