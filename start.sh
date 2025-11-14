#!/bin/sh
set -e

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Collecting Static..."
python manage.py collectstatic --noinput

echo "Seeding data"
python manage.py seed_all

echo "Starting the server..."
gunicorn sikari.wsgi:application --bind 0.0.0.0:8000
