from rest_framework import viewsets, permissions
from apps.core.pagination import CustomPagination
from .models import Project
from .serializers import ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endopoint for projects.
    -Public: Read-only access to PUBLISHED projects.
    -Admin: Full access.
    """

    serializer_class = ProjectSerializer
    pagination_class = CustomPagination
    lookup_field = "slug"

    def get_queryset(self):
        if self.request.user.is_staff:
            return Project.objects.all()

        return Project.objects.published()

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]
