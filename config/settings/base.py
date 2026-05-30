"""
Django settings for the portfolio-backend project.

This is the base settings file. It contains configuration that is common
to all environments (development, production, etc.).

For more information on this file, see
https://docs.djangoproject.com/en/stable/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/stable/ref/settings/
"""

import os
import sys
from datetime import timedelta
from pathlib import Path

from decouple import Csv, config

# --- PATH CONFIGURATION ---
# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR points to the project's root directory.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Add the 'apps' directory to the Python path to allow for cleaner imports.
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))


# --- SECURITY CONFIGURATION ---
# See https://docs.djangoproject.com/en/stable/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# The secret key is used for cryptographic signing.
SECRET_KEY = config(
    "SECRET_KEY",
    default="django-insecure-please-change-me",
)

# SECURITY WARNING: don't run with debug turned on in production!
# Debug mode displays detailed error pages, which can leak sensitive information.
DEBUG = config("DEBUG", default=False, cast=bool)

# A list of allowed host/domain names for this site.
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="", cast=Csv())


# --- APPLICATION DEFINITION ---
# Application definition
INSTALLED_APPS = [
    "corsheaders",
    # Django core apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "cloudinary",
    "django.contrib.staticfiles",
    # Third-party apps
    "rest_framework",
    "rest_framework_simplejwt",
    "djoser",
    # Local apps
    "apps.users.apps.UsersConfig",
    "apps.projects.apps.ProjectsConfig",
    "apps.blog.apps.BlogConfig",
    "apps.contact.apps.ContactConfig",
    "apps.core.apps.CoreConfig",
]

# --- MIDDLEWARE CONFIGURATION ---
# A list of middleware to be executed for each request/response.
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# --- CORS CONFIGURATION ---

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    "accept",
    "authorization",
    "content-type",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]


# --- URL CONFIGURATION ---
# The root URL configuration module.
ROOT_URLCONF = "config.urls"

# --- TEMPLATE CONFIGURATION ---
# Configuration for the template engine.
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# --- WSGI CONFIGURATION ---
# The WSGI application entry point.
WSGI_APPLICATION = "config.wsgi.application"


# --- DATABASE CONFIGURATION ---
# Database configuration is defined in environment-specific files (local.py, production.py). # noqa: E501
# https://docs.djangoproject.com/en/stable/ref/settings/#databases


# --- PASSWORD VALIDATION ---
# https://docs.djangoproject.com/en/stable/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# --- INTERNATIONALIZATION ---
# https://docs.djangoproject.com/en/stable/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# --- FILE UPLOAD CONFIGURATION ---
# Handlers for processing file uploads.
FILE_UPLOAD_HANDLERS = [
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler",
]

# --- STATIC FILES CONFIGURATION ---
# https://docs.djangoproject.com/en/stable/howto/static-files/
STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# --- DEFAULT PRIMARY KEY FIELD TYPE ---
# https://docs.djangoproject.com/en/stable/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- AUTHENTICATION CONFIGURATION ---
# Custom user model for authentication.
AUTH_USER_MODEL = "users.User"

# --- DJANGO REST FRAMEWORK CONFIGURATION ---
REST_FRAMEWORK = {
    # Authentication classes for REST framework.
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    # Default permission classes.
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    # Custom exception handler for consistent error responses.
    "EXCEPTION_HANDLER": "apps.core.exceptions.custom_exception_handler",
    # Custom pagination class.
    "DEFAULT_PAGINATION_CLASS": "apps.core.pagination.CustomPagination",
    "PAGE_SIZE": 10,
}

# --- SIMPLE JWT CONFIGURATION ---
# Configuration for JSON Web Token authentication.
SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("Bearer",),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

# --- DJOSER CONFIGURATION ---
# Configuration for user registration and authentication endpoints.
DJOSER = {
    "LOGIN_FIELD": "email",
    "USER_CREATE_PASSWORD_RETYPE": True,
    "USERNAME_CHANGED_EMAIL_CONFIRMATION": True,
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION": True,
    "SEND_CONFIRMATION_EMAIL": True,
    "SET_USERNAME_RETYPE": True,
    "SET_PASSWORD_RETYPE": True,
    "PASSWORD_RESET_CONFIRM_URL": "password/reset/confirm/{uid}/{token}",
    "USERNAME_RESET_CONFIRM_URL": "email/reset/confirm/{uid}/{token}",
    "ACTIVATION_URL": "activate/{uid}/{token}",
    "SEND_ACTIVATION_EMAIL": True,
    "SERIALIZERS": {
        "user_create": "users.serializers.UserCreateSerializer",
        "user": "users.serializers.UserSerializer",
        "current_user": "users.serializers.UserSerializer",
        "user_delete": "djoser.serializers.UserDeleteSerializer",
    },
}

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

USE_CLOUDINARY = config("USE_CLOUDINARY", default=False, cast=bool)

if USE_CLOUDINARY:
    CLOUDINARY_CREDENTIALS = {
        "cloud_name": config(
            "CLOUDINARY_CLOUD_NAME",
            default="demo",
            cast=str,
        ),
        "api_key": config(
            "CLOUDINARY_API_KEY",
            default="123456789012345",
            cast=str,
        ),
        "api_secret": config(
            "CLOUDINARY_API_SECRET",
            default="abcdefghijklmnopqrstuvwxyz",
            cast=str,
        ),
    }

    CLOUDINARY_STORAGE = {
        "CLOUD_NAME": CLOUDINARY_CREDENTIALS["cloud_name"],
        "API_KEY": CLOUDINARY_CREDENTIALS["api_key"],
        "API_SECRET": CLOUDINARY_CREDENTIALS["api_secret"],
    }

    STORAGES["default"]["BACKEND"] = "cloudinary_storage.storage.MediaCloudinaryStorage"

    CLOUDINARY = CLOUDINARY_CREDENTIALS

MEDIA_URL = config("MEDIA_URL", default="/media/")
MEDIA_ROOT = BASE_DIR / "media"

# --- CACHING CONFIGURATION ---
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "portfolio-backend-cache",
    }
}
CACHE_TIMEOUT = config("CACHE_TIMEOUT", default=900, cast=int)
