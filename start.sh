#!/usr/bin/env bash
set -o errexit

# Go to backend
cd backend

# Run migrations
python manage.py migrate --noinput

# Start Django via gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
