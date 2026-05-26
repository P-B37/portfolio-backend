from rest_framework import serializers

from .models import Project, Technology


class TechnologySerializer(serializers.ModelSerializer):
    """
    Serializer for the Technology model.
    """

    class Meta:
        model = Technology
        fields = ["id", "name", "slug", "icon_name", "category"]
        read_only_fields = ["id", "slug"]


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for the Project model.
    Read-only for public users.
    """

    status_label = serializers.CharField(source="get_status_display", read_only=True)
    technologies = TechnologySerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "slug",
            "summary",
            "content",
            "image",
            "repository_url",
            "live_demo_url",
            "status",
            "status_label",
            "is_featured",
            "created_at",
            "technologies",
        ]
        read_only_fields = ["id", "slug", "created_at", "updated_at"]


class ProjectListSerializer(serializers.ModelSerializer):
    """
    Optimized serializer for Project listing endpoints.
    Excludes the large 'content' (markdown) field to reduce API payload size.
    """

    status_label = serializers.CharField(source="get_status_display", read_only=True)
    technologies = TechnologySerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "slug",
            "summary",
            "image",
            "repository_url",
            "live_demo_url",
            "status",
            "status_label",
            "is_featured",
            "created_at",
            "technologies",
        ]
        read_only_fields = fields
