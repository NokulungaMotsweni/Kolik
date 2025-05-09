from decouple import config  # .env config
from pathlib import Path
from django.utils.translation import gettext_lazy as _
import os
from dotenv import load_dotenv
load_dotenv()


# ========================
# BASE DIRECTORY
# ========================
BASE_DIR = Path(__file__).resolve().parent.parent

# ========================
# SECURITY SETTINGS
# ========================
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', cast=bool)
ALLOWED_HOSTS = []

# ========================
# INSTALLED APPLICATIONS
# ========================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'rest_framework',
    'corsheaders',

    # Local apps
    'users',
    'products',
    'shopping_list',

    # Monitoring/Logging for Middleware
    'monitoring',
]
 
# ========================
# MIDDLEWARE
# ========================
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',   
    'middleware.geolocation_middleware.GeolocationMiddleware', 
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ========================
# URLS & WSGI
# ========================
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

# ========================
# DATABASE (DEV ONLY)
# ========================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ========================
# CUSTOM USER MODEL
# ========================
AUTH_USER_MODEL = 'users.CustomUser'

# ========================
# PASSWORD VALIDATORS
# ========================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ========================
# LOCALIZATION
# ========================
LANGUAGE_CODE = 'en-us'
LANGUAGES = [
    ('en', _('English')),
    ('cs', _('Czech')),
]
TIME_ZONE = 'Europe/Prague'
USE_I18N = True
USE_TZ = True

# ========================
# STATIC & MEDIA
# ========================
STATIC_URL = 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ========================
# TEMPLATES
# ========================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'config' / 'templates'],
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

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ========================
# CORS / CSRF (Frontend)
# ========================
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
]
CSRF_COOKIE_HTTPONLY = False

# ========================
# GEOLOCATION & VPN CONFIG
# ========================
MAXMIND_DB_PATH = BASE_DIR / 'data' / 'GeoLite2-Country.mmdb'
IPINFO_TOKEN = config("IPINFO_TOKEN")
PROXYCHECK_KEY = config("PROXYCHECK_KEY")
REDIRECT_URL = "https://www.visitczechia.com"
DEBUG_IP_OVERRIDE = config("DEBUG_IP_OVERRIDE", default=None)

# ========================
# POLICY VERSIONING
# ========================
COOKIE_POLICY_VERSION = "1.0"

#sendgrid 
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")

#RECAPTCHA
RECAPTCHA_V3_SITE_KEY = os.getenv("RECAPTCHA_V3_SITE_KEY")
RECAPTCHA_V3_SECRET_KEY = os.getenv("RECAPTCHA_V3_SECRET_KEY")

RECAPTCHA_V2_SITE_KEY = os.getenv("RECAPTCHA_V2_SITE_KEY")
RECAPTCHA_V2_SECRET_KEY = os.getenv("RECAPTCHA_V2_SECRET_KEY")