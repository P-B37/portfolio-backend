from decouple import config

from .base import *  # noqa

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

DOMAIN = config("DOMAIN", default="localhost:8000")
SITE_NAME = config("SITE_NAME", default="Portfolio-Backend")

# --- Email Settings ---

# Determine provider dynamically (default to google, fallback to sendgrid)
EMAIL_PROVIDER = config("EMAIL_PROVIDER", default="google").lower()

google_user = config("EMAIL_HOST_USER", default="")
google_password = config("EMAIL_HOST_PASSWORD", default="")

# Auto-fallback to SendGrid if google provider is selected but
# no credentials are provided
if (
    EMAIL_PROVIDER == "google"
    and (not google_user or not google_password or google_password == "password")
    and config("SENDGRID_API_KEY", default="")
):
    EMAIL_PROVIDER = "sendgrid"

if EMAIL_PROVIDER == "google":
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_USE_SSL = False
    EMAIL_HOST_USER = google_user or "bonheurndezenc@gmail.com"
    EMAIL_HOST_PASSWORD = google_password or "password"
else:
    # Use SendGrid HTTPS Web API backend to bypass Render SMTP port blocking
    EMAIL_BACKEND = "apps.core.email_backends.SendGridAPIBackend"
    SENDGRID_API_KEY = config("SENDGRID_API_KEY", default="password")

DEFAULT_FROM_EMAIL = config(
    "DEFAULT_FROM_EMAIL", default=google_user or "bonheurndezenc@gmail.com"
)

# Who receives the contact form? (Your personal email)
ADMIN_EMAIL = config("ADMIN_EMAIL", default="bonheurndezenc@gmail.com")

EMAIL_TIMEOUT = 10
# Security Enhancements
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True

# --- Cache Configuration Overrides ---
DISABLE_CACHE = config("DISABLE_CACHE", default=False, cast=bool)
if DISABLE_CACHE:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        }
    }
    CACHE_TIMEOUT = 0
