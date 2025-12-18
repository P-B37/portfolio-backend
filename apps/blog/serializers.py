from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    # display the author' full name or email/username instead of an ID number
    author = serializers.StringRelatedField(
        read_only=True,
    )
    status_label = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "title",
            "slug",
            "summary",
            "content",
            "image",
            "reading_time",
            "status",
            "status_label",
            "created_at",
            "updated_at",
        ]

        read_only_fields = ["id", "slug", "reading_time", "created_at", "updated_at"]
