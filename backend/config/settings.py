from decouple import config  # Loads secrets from .env file
from pathlib import Path  # Helps manage file paths
from django.utils.translation import gettext_lazy as _  # For multilingual support

# Base directory for the project 
BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings
SECRET_KEY = config('SECRET_KEY')  # NEVER hardcode this key
DEBUG = config('DEBUG', cast=bool)  # Set to False in production!
ALLOWED_HOSTS = []  # We will add IP/domain names when deploying

# Installed Django apps
INSTALLED_APPS = [
    'django.contrib.admin',           # Admin interface
    'django.contrib.auth',            # User authentication
    'django.contrib.contenttypes',    # Content type system
    'django.contrib.sessions',        # Session framework
    'django.contrib.messages',        # Messaging framework
    'django.contrib.staticfiles',     # Serving static files
    'core',                           # Our custom app
    'rest_framework',                 # Django REST Framework for APIs
]

# Middleware - handles requests and responses
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

#  Main URL config and WSGI app
ROOT_URLCONF = 'config.urls'  # Points to our main routing file
WSGI_APPLICATION = 'config.wsgi.application'  # Used for deployment

# Database setup (SQLite for now; PostgreSQL later for deployment)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Simple local DB
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 🔑 Password validators (standard Django defaults)
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization (Multilingual Support)
LANGUAGE_CODE = 'en-us'  # Default language

LANGUAGES = [  # Supported languages in the app
    ('en', _('English')),
    ('cs', _('Czech')),
]

TIME_ZONE = 'Europe/Prague'  # Local time zone

USE_I18N = True  # Enable translation system
USE_TZ = True    # Enable timezone-aware datetimes

# Static files (CSS, JavaScript, admin styles)
STATIC_URL = 'static/'  # Where static files are served from during development


# Media files (user uploads product images)
MEDIA_URL = '/media/'  # URL to access uploaded media
MEDIA_ROOT = BASE_DIR / 'media'  # Folder where uploaded media gets stored

# Default primary key type for all models
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#  Templates (used by admin and custom pages)
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