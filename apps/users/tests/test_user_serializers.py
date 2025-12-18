"""
Tests for the User serializers.

This module contains tests for the user-related serializers, ensuring
that they correctly validate and serialize user data.
"""

import pytest
from apps.users.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestUserCreateSerializer:
    """
    Test suite for the UserCreateSerializer.

    This test suite validates the functionality of the UserCreateSerializer,
    including data validation and user instance creation.
    """

    def test_serializer_with_valid_data(self):
        """
        Ensures the serializer is valid when provided with correct data.
        """
        data = {
            "email": "test.user@example.com",
            "password": "complexpassword123",
            "re_password": "complexpassword123",
            "first_name": "Test",
            "last_name": "User",
        }

        serializer = UserCreateSerializer(data=data)
        assert serializer.is_valid(raise_exception=True)

    def test_serializer_creates_user(self):
        """
        Ensures the serializer correctly creates a new user instance.
        """
        data = {
            "email": "test.user@example.com",
            "password": "complexpassword123",
            "re_password": "complexpassword123",
            "first_name": "Test",
            "last_name": "User",
        }

        serializer = UserCreateSerializer(data=data)
        assert serializer.is_valid(raise_exception=True)
        user = serializer.save()

        assert isinstance(user, User)
        assert user.email == data["email"]
        assert user.first_name == data["first_name"]
        assert user.last_name == data["last_name"]
        assert user.check_password(data["password"])

    def test_serializer_with_invalid_email(self):
        """
        Ensures the serializer fails validation with an invalid email format.
        """
        data = {
            "email": "invalid-email",
            "password": "complexpassword123",
            "re_password": "complexpassword123",
        }

        serializer = UserCreateSerializer(data=data)

        assert not serializer.is_valid()
        assert "email" in serializer.errors

    def test_serializer_with_mismatched_passwords(self):
        """
        Ensures the serializer fails validation when passwords do not match.
        """
        data = {
            "email": "test.user@example.com",
            "password": "complexpassword123",
            "re_password": "differentpassword",
        }

        serializer = UserCreateSerializer(data=data)

        assert not serializer.is_valid()
        assert "re_password" in serializer.errors

    def test_serializer_with_missing_email(self):
        """
        Ensures the serializer fails validation if the email is not provided.
        """
        data = {
            "password": "complexpassword123",
            "re_password": "complexpassword123",
        }

        serializer = UserCreateSerializer(data=data)

        assert not serializer.is_valid()
        assert "email" in serializer.errors
