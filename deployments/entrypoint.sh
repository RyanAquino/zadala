#!/bin/sh

poetry run python manage.py migrate --no-input
poetry run python manage.py collectstatic --no-input

DJANGO_SUPERUSER_PASSWORD=$SUPER_USER_PASSWORD poetry run python manage.py createsuperuser --first_name $SUPER_FIRST_NAME --last_name $SUPER_LAST_NAME --email $SUPER_USER_EMAIL --noinput

poetry run gunicorn zadalaAPI.wsgi --bind 0.0.0.0:8000 --workers=$GUNICORN_WORKERS
