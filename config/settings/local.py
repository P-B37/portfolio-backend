import os

from decouple import config

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

CORS_ALLOW_ALL_ORIGINS = config("CORS_ALLOW_ALL_ORIGINS", default=True, cast=bool)

# Database
# https://docs.djangoproject.com/en/stable/ref/settings/#databases
if os.environ.get("DB_ENGINE") == "django.db.backends.postgresql":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": config("DB_NAME", default="postgres"),
            "USER": config("DB_USER", default="postgres"),
            "PASSWORD": config("DB_PASSWORD", default="postgres"),
            "HOST": config("DB_HOST", default="localhost"),
            "PORT": config("DB_PORT", default="5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Email Backend (Prints emails to console instead of sending them)
# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DEFAULT_FROM_EMAIL = config(
    "EMAIL_HOST_USER",
    default="noreply@localhost",
)
DOMAIN = config("DOMAIN", default="localhost:8000")
SITE_NAME = config("SITE_NAME", default="Portfolio-Backend")

# --- Email Settings ---
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"  # Or smtp.sendgrid.net
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Read from Environment Variables (Security Best Practice)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="noreply@localhost")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="password")

# Who receives the contact form? (Your personal email)
ADMIN_EMAIL = config("ADMIN_EMAIL", default="noreply@localhost")

# Disable caching in development if requested (defaults to True for debugging)
DISABLE_CACHE = config("DISABLE_CACHE", default=True, cast=bool)
if DISABLE_CACHE:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        }
    }
    CACHE_TIMEOUT = 0
