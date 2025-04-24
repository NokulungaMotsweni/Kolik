"""
Django settings for the Kolik backend project.

This configuration file defines the core setup of the Django backend,
including installed apps, database settings, middleware, static/media paths,
internationalization, and REST framework integration.

Sensitive values (e.g., SECRET_KEY) are stored securely in a .env file
and loaded using python-decouple for safe development and deployment.
"""

from decouple import config  # .env file
from pathlib import Path  # Manages file system paths
from django.utils.translation import gettext_lazy as _  # Translation

# Base directory of the project 
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY SETTINGS
SECRET_KEY = config('SECRET_KEY')  
DEBUG = config('DEBUG', cast=bool)  # Enable debug mode in development only!
ALLOWED_HOSTS = []  # We have to add domain names or IPs before deploying to production


# INSTALLED APPLICATIONS
INSTALLED_APPS = [
    'django.contrib.admin',           # Django admin site
    'django.contrib.auth',            # Authentication system
    'django.contrib.contenttypes',    # Handles content types
    'django.contrib.sessions',        # Session framework
    'django.contrib.messages',        # Messaging framework
    'django.contrib.staticfiles',     # Serves static files (CSS, JS)
    
    # Third-party apps
    'rest_framework',                 # Django REST Framework for building APIs

    # Local apps
    'users',                          # Handles authentication and user management
    'products',                       # Product catalog, comparisons
    'shopping_cart',                  # Shopping cart and basket logic
]


# MIDDLEWARE CONFIGURATION
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Security enhancements
    'django.contrib.sessions.middleware.SessionMiddleware',  # Session handling
    'django.middleware.common.CommonMiddleware',  # General request/response handling
    'django.middleware.csrf.CsrfViewMiddleware',  # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Authentication handling
    'django.contrib.messages.middleware.MessageMiddleware',  # Messaging support
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Prevents clickjacking
]


# URL AND WSGI CONFIG
ROOT_URLCONF = 'config.urls'  # Project-level URL configuration
WSGI_APPLICATION = 'config.wsgi.application'  # WSGI entry point for deployment


# DATABASE CONFIGURATION
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Default dev database, later on we will move to postgres for deployment
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# AUTHENTICATION SETTINGS
AUTH_USER_MODEL = 'users.CustomUser'  # Use custom user model from `users` app


# PASSWORD VALIDATION
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# INTERNATIONALIZATION
LANGUAGE_CODE = 'en-us'  # Default language

LANGUAGES = [
    ('en', _('English')),
    ('cs', _('Czech')),  # Added czech
]

TIME_ZONE = 'Europe/Prague'
USE_I18N = True  # Enable translation engine
USE_TZ = True    # Store datetimes in UTC


# STATIC AND MEDIA FILES
STATIC_URL = 'static/'  # URL path to serve static files

MEDIA_URL = '/media/'  # URL path to serve media files (uploaded)
MEDIA_ROOT = BASE_DIR / 'media'  # Where uploaded files are stored


# TEMPLATES CONFIGURATION
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


# DEFAULTS
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'  # Default for model primary keys



# --- CORS HEADERS (Frontend Integration) ---
# Allow React frontend (Vite) at localhost:5173 to connect to this backend
INSTALLED_APPS += ['corsheaders']

# Must come FIRST in the middleware stack
MIDDLEWARE.insert(0, 'corsheaders.middleware.CorsMiddleware')

# Allow frontend to send cookies (for login sessions)
CORS_ALLOW_CREDENTIALS = True

# Allow only this frontend origin (for dev)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]

# CSRF protection for POST/PUT requests from frontend
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
]
