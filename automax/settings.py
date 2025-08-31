import os
from pathlib import Path
import dj_database_url
import environ

# Load environment variables
env = environ.Env(
    DJANGOAPPMODE=(str, "Debug"),
    USEDEBUGDB=(bool, True),
)

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env file (only in local dev)
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# ===============================
# 🔐 Security
# ===============================
SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DJANGOAPPMODE") == "Debug"

# Allowed hosts (local + Render)
ALLOWED_HOSTS = env.list(
    "ALLOWED_HOSTS",
    default=["127.0.0.1", "localhost", ".onrender.com"],
)

# ===============================
# 📦 Installed Apps & Middleware
# ===============================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # add your apps here
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
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
        "DIRS": [BASE_DIR / "templates"],
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

# ===============================
# 🗄️ Database
# ===============================
if env.bool("USEDEBUGDB", default=True):
    # SQLite (local dev)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    # Postgres (Render)
    DATABASES = {
        "default": dj_database_url.config(
            default=f"postgres://{env('DBUSER')}:{env('DBPASSWORD')}@{env('DBHOST')}:{env('DBPORT')}/{env('DBNAME')}",
            conn_max_age=600,
            ssl_require=True,
        )
    }

# ===============================
# 🔤 Password Validation
# ===============================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ===============================
# 🌍 Internationalization
# ===============================
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ===============================
# 🖼️ Static & Media Files
# ===============================
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ===============================
# 📧 Email
# ===============================
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"  # change if using Mailgun/SendGrid
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="dummy@example.com")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="dummy")

# ===============================
# ✅ Default Primary Key
# ===============================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
