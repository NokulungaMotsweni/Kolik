from decouple import config #lets us load secrets from .env
from pathlib import Path #handles file paths
from django.utils.translation import gettext_lazy as _

# Base directory for the project (where manage.py lives)
BASE_DIR = Path(__file__).resolve().parent.parent

# Security stuff - used for security, detailed errors, list of domains/IPs allowed to access the site
SECRET_KEY = config('SECRET_KEY')  # NEVER HARDCODE
DEBUG = config('DEBUG', cast=bool)
ALLOWED_HOSTS = []  # will be updated for deployment

# Installed apps - default apps, third party apps, own apps like products, users
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'rest_framework',
]

# pipeline that processes every request and response eg: session handling, CSRF protection, authentication, security headers - almost never changes unless we want to add special stuff
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'config.urls' # tells Django where main urls.py is
WSGI_APPLICATION = 'config.wsgi.application' # entry point for production servers (like Render)

# Database config — using SQLite for now (will switch to PostgreSQL later)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation (pretty standard)
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Language and timezone
LANGUAGE_CODE = 'en-us'
LANGUAGES = [
    ('en', _('English')),
    ('cs', _('Czech')),
]
TIME_ZONE = 'Europe/Prague'

USE_I18N = True
USE_TZ = True

# Static files (CSS, JS, images)
STATIC_URL = 'static/'

# Default ID field type for models
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#Load template files (for admin, pages, etc.) and handles dynamic content like user data
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

#tells Django to store images
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'