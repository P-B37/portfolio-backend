from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Category, Post, Tag

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]
        read_only_fields = ["id", "slug"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]
        read_only_fields = ["id", "slug"]


class PostSerializer(serializers.ModelSerializer):
    # display the author' full name or email/username instead of an ID number
    author = serializers.StringRelatedField(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    status_label = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "category",
            "tags",
            "title",
            "slug",
            "summary",
            "content",
            "image",
            "reading_time",
            "status",
            "status_label",
            "views_count",
            "likes_count",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "slug",
            "reading_time",
            "views_count",
            "likes_count",
            "created_at",
            "updated_at",
        ]


class BlogPostListSerializer(serializers.ModelSerializer):
    """
    Optimized serializer for Blog Post listing endpoints.
    Excludes the large 'content' (markdown) field to reduce API payload size.
    """

    author = serializers.StringRelatedField(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    status_label = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "category",
            "tags",
            "title",
            "slug",
            "summary",
            "image",
            "reading_time",
            "status",
            "status_label",
            "views_count",
            "likes_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields
