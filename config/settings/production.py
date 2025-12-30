from .base import *  # noqa
from decouple import config

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS", default="", cast=lambda v: [s.strip() for s in v.split(",")]
)

CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS", default="", cast=lambda v: [s.strip() for s in v.split(",")]
)

# Database - PostgreSQL
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("PGDATABASE", default="postgres"),
        "USER": config("PGUSER", default="postgres"),
        "PASSWORD": config("PGPASSWORD", default="postgres"),
        "HOST": config("PGHOST", default="localhost"),
        "PORT": config("PGPORT", default="5432"),
        "CONN_MAX_AGE": int(config("CONN_MAX_AGE", default=30)),
        "CONN_HEALTH_CHECKS": bool(config("CONN_HEALTH_CHECKS", default=False)),
        "OPTIONS": {
            "sslmode": "require",
        },
        "DISABLE_SERVER_SIDE_CURSORS": True,
    }
}

DEFAULT_FROM_EMAIL = config(
    "EMAIL_HOST_USER",
    default="noreply@localhost",
)
DOMAIN = config("DOMAIN", default="localhost:8000")
SITE_NAME = config("SITE_NAME", default="Portfolio-Backend")

# --- Email Settings ---
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_PORT = 2525
EMAIL_USE_TLS = True

# Read from Environment Variables (Security Best Practice)
EMAIL_HOST_USER = "apikey"
EMAIL_HOST_PASSWORD = config("SENDGRID_API_KEY", default="password")

# Who receives the contact form? (Your personal email)
ADMIN_EMAIL = config("ADMIN_EMAIL", default="noreply@localhost")
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

EMAIL_USE_TLS = True
# ADD THIS: Explicitly tell Django not to use implicit SSL (mutually exclusive with TLS)
EMAIL_USE_SSL = False

EMAIL_TIMEOUT = 10
# Security Enhancements
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
