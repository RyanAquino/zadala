#!/bin/sh

python manage.py migrate --no-input
python manage.py collectstatic --no-input

DJANGO_SUPERUSER_PASSWORD=$SUPER_USER_PASSWORD python manage.py createsuperuser --first_name $SUPER_FIRST_NAME --last_name $SUPER_LAST_NAME --email $SUPER_USER_EMAIL --noinput

gunicorn zadalaAPI.wsgi --bind 0.0.0.0:8000 --workers=$GUNICORN_WORKERS
