"""
Tests for the custom User model.

This module contains tests for the User model, ensuring that its
custom functionalities, such as email-based authentication and soft
deletion, work as expected.
"""
import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()


@pytest.mark.django_db
class TestUserModel:
    """
    Test suite for the custom User model.

    This test suite covers the creation of regular users and superusers,
    as well as the soft deletion and restoration functionality.
    """

    def test_create_user_successful(self):
        """
        Ensures a new user can be created successfully with an email and password.
        """
        user = User.objects.create_user(
            email="test.user@example.com",
            password="complexpassword123"
        )

        assert user.email == "test.user@example.com"
        assert user.check_password("complexpassword123")
        assert user.is_active
        assert not user.is_staff
        assert not user.is_superuser
        assert not user.is_deleted

    def test_create_user_without_email_raises_error(self):
        """
        Ensures that creating a user without an email raises a ValueError.
        """
        with pytest.raises(ValueError, match="The Email must be set"):
            User.objects.create_user(email=None, password="password123")

    def test_create_superuser_successful(self):
        """
        Ensures a new superuser can be created successfully.
        """
        superuser = User.objects.create_superuser(
            email="superuser@example.com",
            password="supersecretpassword"
        )

        assert superuser.email == "superuser@example.com"
        assert superuser.check_password("supersecretpassword")
        assert superuser.is_active
        assert superuser.is_staff
        assert superuser.is_superuser
        assert not superuser.is_deleted

    def test_create_superuser_without_staff_flag_raises_error(self):
        """
        Ensures that creating a superuser with is_staff=False raises a ValueError.
        """
        with pytest.raises(ValueError, match="Superuser must have is_staff=True."):
            User.objects.create_superuser(
                email="superuser@example.com",
                password="supersecretpassword",
                is_staff=False
            )

    def test_create_superuser_without_superuser_flag_raises_error(self):
        """
        Ensures that creating a superuser with is_superuser=False raises a ValueError.
        """
        with pytest.raises(ValueError, match="Superuser must have is_superuser=True."):
            User.objects.create_superuser(
                email="superuser@example.com",
                password="supersecretpassword",
                is_superuser=False
            )

    def test_user_email_is_unique(self):
        """
        Ensures that the email field is unique and raises an IntegrityError
        for duplicate emails.
        """
        User.objects.create_user(email="test.user@example.com", password="password123")
        with pytest.raises(IntegrityError):
            User.objects.create_user(email="test.user@example.com", password="password456")

    def test_soft_delete_user(self):
        """
        Ensures that the delete() method performs a soft delete.
        """
        user = User.objects.create_user(
            email="delete.me@example.com",
            password="testpass123"
        )
        user.delete()

        # The user should not be in the default manager's queryset.
        assert not User.objects.filter(email="delete.me@example.com").exists()

        # The user should exist in the all_objects manager's queryset.
        deleted_user = User.all_objects.get(pk=user.pk)
        assert deleted_user.is_deleted
        assert deleted_user.deleted_at is not None

    def test_restore_soft_deleted_user(self):
        """
        Ensures that a soft-deleted user can be restored.
        """
        user = User.objects.create_user(
            email="restore.me@example.com",
            password="testpass123"
        )
        user.delete()
        user.restore()

        # The user should be back in the default manager's queryset.
        restored_user = User.objects.get(pk=user.pk)
        assert not restored_user.is_deleted
        assert restored_user.deleted_at is None

    def test_hard_delete_user(self):
        """
        Ensures that the hard_delete() method permanently deletes a user.
        """
        user = User.objects.create_user(
            email="hard.delete@example.com",
            password="testpass123"
        )
        user_id = user.id
        user.hard_delete()

        # The user should not exist in any manager's queryset.
        assert not User.all_objects.filter(id=user_id).exists()

    def test_user_str_representation(self):
        """
        Ensures the string representation of a user is their email address.
        """
        user = User.objects.create_user(
            email="string.rep@example.com",
            password="testpass123"
        )
        assert str(user) == "string.rep@example.com"