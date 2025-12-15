"""
Custom User model for the application.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import SoftDeleteModel
from .managers import CustomUserManager


class User(SoftDeleteModel, AbstractUser):
    """
    Custom user model that uses email as the unique identifier for authentication.

    This model inherits from `SoftDeleteModel` to support soft deletion and
    `AbstractUser` for Django's authentication framework.
    """
    # Remove the username field from the default AbstractUser model.
    username = None
    # Use email as the unique identifier for authentication.
    email = models.EmailField(_("email address"), unique=True)

    # Set the email field as the username field for authentication.
    USERNAME_FIELD = "email"
    # No additional fields are required for user creation. Email and password are required by default.
    REQUIRED_FIELDS = []

    # Use the custom manager for this user model.
    objects = CustomUserManager()

    def __str__(self):
        """
        Returns the email address as the string representation of the user.
        """
        return self.email
