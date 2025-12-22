from rest_framework.viewsets import ReadOnlyModelViewSet
from apps.core.pagination import CustomPagination
from apps.core.permissions import IsAdminOrReadOnly
from .models import Project
from .serializers import ProjectSerializer


class ProjectViewSet(ReadOnlyModelViewSet):
    """
    API endopoint for projects.
    -Public: Read-only access to PUBLISHED projects.
    -Admin: Full access.
    """

    serializer_class = ProjectSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"

    def get_queryset(self):
        if self.request.user.is_staff:
            return Project.objects.all()

        return Project.objects.published()


class ProjectFeaturedViewSet(ReadOnlyModelViewSet):
    """
    API endopoint for projects.
    -Public: Read-only access to PUBLISHED projects.
    -Admin: Full access.
    """

    serializer_class = ProjectSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"

    def get_queryset(self):
        if self.request.user.is_staff:
            return Project.objects.all()

        return Project.objects.published().featured()
