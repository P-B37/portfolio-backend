from rest_framework import serializers
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for the Project model.
    Read-only for public users.
    """

    # Custom read-only field to explicitly get
    # the 'Draft'/'Published' label if needed
    status_label = serializers.CharField(source="get_status_display", read_only=True)

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
        ]
        read_only_fields = ["id", "slug", "created_at", "updated_at"]
