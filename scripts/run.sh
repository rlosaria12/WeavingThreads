#!/bin/sh

set -e

# Wait for the database
python manage.py wait_for_db

# Collect static files
python manage.py collectstatic --noinput

# Apply database migrations
python manage.py migrate

# Start uwsgi
uwsgi --socket :9000 --workers 4 --master --enable-threads --module app.wsgi 