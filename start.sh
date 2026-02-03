#!/bin/bash

# Navigate to backend folder
cd backend

# Install dependencies
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

# Run migrations
python3 manage.py migrate

# Start server
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
