#!/bin/bash
cd backend
# Install dependencies
pip install -r requirements.txt
# Run migrations
python manage.py migrate
# Start server
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
