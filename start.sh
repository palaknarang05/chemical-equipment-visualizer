#!/bin/bash

cd backend

python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

python3 manage.py migrate

gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
