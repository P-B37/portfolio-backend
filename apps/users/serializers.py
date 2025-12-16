from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreateSerializer(BaseUserCreateSerializer):
    # Explicit definition to satisfy DRF
    re_password = serializers.CharField(
        style={"input_type": "password"}, write_only=True, required=True
    )

    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ("id", "email", "password", "re_password", "first_name", "last_name")

    def validate(self, attrs):
        # 1. Manually check if passwords match
        if attrs.get("password") != attrs.get("re_password"):
            # We raise the error on 're_password' to match your test expectations
            raise serializers.ValidationError(
                {"re_password": "Passwords do not match."}
            )

        # 2. Remove re_password so it doesn't break the Model instantiation
        # Djoser/Django will crash if we pass this non-model field to User(**attrs)
        attrs.pop("re_password", None)

        # 3. Call parent validation (for email uniqueness, etc.)
        return super().validate(attrs)


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ("id", "email", "first_name", "last_name", "is_active", "date_joined")
