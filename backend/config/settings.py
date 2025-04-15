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