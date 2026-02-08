"""
Django settings for Chemical Equipment Visualizer project.
"""

import os
import dj_database_url
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# =======================
# Security
# =======================
SECRET_KEY = 'django-insecure-chemical-equipment-visualizer-secret-key-2024'
DEBUG = False
ALLOWED_HOSTS = ['*']  # For Render deployment

# =======================
# Installed apps
# =======================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',

    'equipment_api.apps.EquipmentApiConfig',
]

# =======================
# Middleware
# =======================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# =======================
# URLs & WSGI
# =======================
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

# =======================
# Templates
# =======================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# =======================
# Database
# =======================
# Use DATABASE_URL env variable for Postgres, fallback to SQLite locally
DATABASES = {
    'default': dj_database_url.parse(
        os.getenv('DATABASE_URL', f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
        conn_max_age=600
    )
}

# =======================
# Password validation
# =======================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# =======================
# Internationalization
# =======================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# =======================
# Static files
# =======================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# =======================
# Media files
# =======================
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# =======================
# Default primary key
# =======================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =======================
# REST Framework
# =======================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# =======================
# CORS settings
# =======================
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# =======================
# File upload settings
# =======================
UPLOAD_DIR = BASE_DIR / 'equipment_api' / 'uploads'
REPORTS_DIR = BASE_DIR / 'equipment_api' / 'reports'

# Create directories if they don't exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(MEDIA_ROOT, exist_ok=True)