"""
Django settings for automax project.
Optimized for deployment on Render.
"""

import os
from pathlib import Path
import environ
from django.contrib.messages import constants as messages

# -------------------------------------------------------------------
# Base settings
# -------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# Environment variables
env = environ.Env(
    DEBUG=(bool, False),
    USEDEBUGDB=(bool, True),
)
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# Security
SECRET_KEY = env("SECRET_KEY", default="unsafe-secret-key")  # change in production
DEBUG = env("DJANGOAPPMODE", default="Debug") == "Debug"
print(f"Application running in debug mode: {DEBUG}")

# -------------------------------------------------------------------
# Hosts
# -------------------------------------------------------------------
# Example: DJANGO_ALLOWED_HOSTS=automax.onrender.com localhost 127.0.0.1
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["127.0.0.1", "localhost"])

# -------------------------------------------------------------------
# Installed apps
# -------------------------------------------------------------------
INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party apps
    "localflavor",
    "crispy_forms",
    "crispy_bootstrap4",
    "django_filters",

    # Project apps
    "main",
    "users",
]

# -------------------------------------------------------------------
# Middleware
# -------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Static file optimization
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# -------------------------------------------------------------------
# URLs and WSGI
# -------------------------------------------------------------------
ROOT_URLCONF = "automax.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],  # global templates
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "automax.wsgi.application"

# -------------------------------------------------------------------
# Database
# -------------------------------------------------------------------
if env("USEDEBUGDB", default=True):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": env("DBNAME"),
            "USER": env("DBUSER"),
            "PASSWORD": env("DBPASSWORD"),
            "HOST": env("DBHOST"),
            "PORT": env("DBPORT"),
        }
    }

# -------------------------------------------------------------------
# Authentication & Login
# -------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LOGIN_REDIRECT_URL = "/home/"
LOGIN_URL = "/login/"

# -------------------------------------------------------------------
# Messages
# -------------------------------------------------------------------
MESSAGE_TAGS = {
    messages.ERROR: "danger"
}

# -------------------------------------------------------------------
# Internationalization
# -------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# -------------------------------------------------------------------
# Static & Media files
# -------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# -------------------------------------------------------------------
# Optional: AWS S3 storage (for production media)
# -------------------------------------------------------------------
DEFAULT_FILE_STORAGE = env(
    "DEFAULT_FILE_STORAGE",
    default="django.core.files.storage.FileSystemStorage"
)

AWS_ACCESS_KEY_ID = env("BUCKETEER_AWS_ACCESS_KEY_ID", default="")
AWS_SECRET_ACCESS_KEY = env("BUCKETEER_AWS_SECRET_ACCESS_KEY", default="")
AWS_S3_REGION_NAME = env("BUCKETEER_AWS_REGION", default="")
AWS_STORAGE_BUCKET_NAME = env("BUCKETEER_BUCKET_NAME", default="")

# -------------------------------------------------------------------
# Crispy Forms
# -------------------------------------------------------------------
CRISPY_TEMPLATE_PACK = "bootstrap4"

# -------------------------------------------------------------------
# Email
# -------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST", default="smtp.mailgun.org")
EMAIL_PORT = env("EMAIL_PORT", default=587)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="dummy@example.com")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="dummy")

# -------------------------------------------------------------------
# Default primary key field type
# -------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
