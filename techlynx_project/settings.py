"""
Django settings for techlynx_project project.

Generated for Techlynx Pro - Professional IT Services Website
"""

from pathlib import Path
import os
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


def _resolve_sqlite_path() -> Path:
    """Keep SQLite outside MEDIA_ROOT/STATIC_ROOT; optional SQLITE_PATH env override."""
    env_path = config('SQLITE_PATH', default='').strip()
    if env_path:
        p = Path(env_path)
        if not p.is_absolute():
            p = BASE_DIR / p
        p.parent.mkdir(parents=True, exist_ok=True)
        return p
    legacy = BASE_DIR / 'db.sqlite3'
    private_db = BASE_DIR / 'private' / 'db.sqlite3'
    if legacy.is_file():
        return legacy
    private_db.parent.mkdir(parents=True, exist_ok=True)
    return private_db


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-this-in-production-to-secure-random-key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

# ALLOWED_HOSTS - Set specific domains in production
# Supports: http://techlynxpro.com, https://techlynxpro.com, www.techlynxpro.com
ALLOWED_HOSTS = [h.strip() for h in config('ALLOWED_HOSTS', default='localhost,127.0.0.1,techlynxpro.com,www.techlynxpro.com,3.82.24.132').split(',') if h.strip()]

# HTTPS origins for CSRF when behind a reverse proxy / alternate hostnames (comma-separated).
_csrf_origins = config('CSRF_TRUSTED_ORIGINS', default='', cast=str).strip()
CSRF_TRUSTED_ORIGINS = [o.strip() for o in _csrf_origins.split(',') if o.strip()]

# Gemini API Configuration
GEMINI_API_KEY = config('GEMINI_API_KEY', default='')
GEMINI_MODEL = config('GEMINI_MODEL', default='gemini-2.0-flash')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',  # Sitemap support
    'website',  # Main website app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'website.middleware.RejectSuspiciousPathMiddleware',
    'website.middleware.SecurityHeadersMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Compressed static files when Django serves /static/
    'django.middleware.gzip.GZipMiddleware',  # Compress HTML from views (nginx /static/ bypasses this)
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'techlynx_project.urls'

# Avoid exposing template debug info when DEBUG is False.
_template_context_processors = [
    'django.template.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.template.context_processors.media',
    'website.context_processors.site_seo',
]
if DEBUG:
    _template_context_processors.insert(0, 'django.template.context_processors.debug')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': _template_context_processors,
        },
    },
]

WSGI_APPLICATION = 'techlynx_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': _resolve_sqlite_path(),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Pre-compress JS/CSS at collectstatic (.gz siblings) — nginx gzip_static serves them; fixes PageSpeed "uncompressed assets"
STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage',
    },
}

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Security Settings
# =================

# XSS Protection
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'  # Prevent clickjacking

# CSRF Protection
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = not DEBUG  # Only secure in production
CSRF_USE_SESSIONS = False
CSRF_COOKIE_SAMESITE = 'Lax'

# Session Security
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = not DEBUG  # Only secure in production
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_SAVE_EVERY_REQUEST = True  # Prevent session fixation

# Password Security
PASSWORD_RESET_TIMEOUT = 3600  # 1 hour

# Security Headers (Production only)
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Additional Security
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# Isolate browsing context (helps against some cross-origin attacks)
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin'

# Admin Security — set ADMIN_PATH in env (e.g. "manage-tlx/") to avoid default /admin/ guess
ADMIN_PATH = config('ADMIN_PATH', default='admin/')
if not ADMIN_PATH.endswith('/'):
    ADMIN_PATH = ADMIN_PATH + '/'

# Data Validation
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB max upload
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB max file upload
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000  # Prevent DoS via form fields

# Email Backend (if using email)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # Development only

# Logging Security - Don't log sensitive data
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}
