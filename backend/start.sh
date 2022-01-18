#!/bin/sh

cd /backend/drinkif/

python3 manage.py migrate


service nginx status
service nginx start
service nginx status

echo "Version 1.1"

pip3 install -r /backend/requirements.txt


echo "Starting Gunicorn..."
gunicorn --bind 0.0.0.0:8000 drinkif.wsgi 