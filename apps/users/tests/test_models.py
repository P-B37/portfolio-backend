import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestUserModel:
    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = "test@example.com"
        password = "testpass123"
        user = User.objects.create_user(email=email, password=password)

        assert user.email == email
        assert user.check_password(password) is True
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False
        assert user.is_deleted is False
    
    def test_create_user_without_email_raises_error(self):
        with pytest.raises(ValueError) as excinfo:
            User.objects.create_user(email=None, password="password123")

        assert str(excinfo.value) == "The Email must be set"

    def test_soft_delete_user(self):
        """Test soft deleting a user"""
        
        user = User.objects.create_user(
            email="delete@example.com",
            password="testpass123")
        
        # perform soft delete
        user.delete()

        # step 1 ensure user is no longer in the standard queryset
        assert User.objects.filter(email="delete@example.com").exists() is False

        # step 2 ensure user still exists in the 'all_objects' queryset
        deleted_user = User.all_objects.get(pk=user.pk)
        assert deleted_user.is_deleted is True
        assert deleted_user.deleted_at is not None

        