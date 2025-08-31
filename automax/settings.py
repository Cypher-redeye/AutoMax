"""
Django settings for AutoMax project (Render-ready).
"""

import os
from pathlib import Path
import environ
from django.contrib.messages import constants as messages

# ------------------------------------------------------------------------------
# BASE & ENVIRONMENT
# ------------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False),
    USEDEBUGDB=(bool, True),
)
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# ------------------------------------------------------------------------------
# SECURITY
# ------------------------------------------------------------------------------
SECRET_KEY = env("SECRET_KEY", default="changeme-secret-key")

DEBUG = env("DJANGOAPPMODE", default="Debug") == "Debug"
print(f"Application running in debug mode: {DEBUG}")

# Allowed hosts (local + env for Render)
ALLOWED_HOSTS = env.list(
    "ALLOWED_HOSTS",
    default=[
        "127.0.0.1",
        "localhost",
        ".onrender.com",   # allow any Render subdomain
    ],
)

# ------------------------------------------------------------------------------
# APPLICATIONS
# ------------------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "localflavor",
    "crispy_forms",
    "crispy_bootstrap4",
    "django_filters",

    # Your apps
    "main",
    "users",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # static files on Render
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "automax.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # global templates folder
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

# ------------------------------------------------------------------------------
# DATABASE
# ------------------------------------------------------------------------------
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

# ------------------------------------------------------------------------------
# AUTH & USER
# ------------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LOGIN_REDIRECT_URL = "/home/"
LOGIN_URL = "/login/"

# ------------------------------------------------------------------------------
# MESSAGES
# ------------------------------------------------------------------------------
MESSAGE_TAGS = {messages.ERROR: "danger"}

# ------------------------------------------------------------------------------
# INTERNATIONALIZATION
# ------------------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ------------------------------------------------------------------------------
# STATIC & MEDIA
# ------------------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ------------------------------------------------------------------------------
# STORAGE (optional: AWS S3, set env vars to activate)
# ------------------------------------------------------------------------------
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
AWS_ACCESS_KEY_ID = env("BUCKETEER_AWS_ACCESS_KEY_ID", default="")
AWS_SECRET_ACCESS_KEY = env("BUCKETEER_AWS_SECRET_ACCESS_KEY", default="")
AWS_S3_REGION_NAME = env("BUCKETEER_AWS_REGION", default="")
AWS_STORAGE_BUCKET_NAME = env("BUCKETEER_BUCKET_NAME", default="")

# ------------------------------------------------------------------------------
# CRISPY FORMS
# ------------------------------------------------------------------------------
CRISPY_TEMPLATE_PACK = "bootstrap4"

# ------------------------------------------------------------------------------
# EMAIL
# ------------------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.mailgun.org"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")

# ------------------------------------------------------------------------------
# DEFAULT PRIMARY KEY FIELD
# ------------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
