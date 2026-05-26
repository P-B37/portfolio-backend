from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets

from apps.core.pagination import CustomPagination
from apps.core.permissions import IsAdminOrReadOnly

from .models import Project
from .serializers import ProjectListSerializer, ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint for projects.
    - Public: Read-only access to PUBLISHED projects.
    - Admin: Full access (CRUD).
    """

    pagination_class = CustomPagination
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"

    @method_decorator(cache_page(settings.CACHE_TIMEOUT))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(settings.CACHE_TIMEOUT))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == "list":
            return ProjectListSerializer
        return ProjectSerializer

    def get_queryset(self):
        queryset = Project.objects.prefetch_related("technologies")
        if self.request.user.is_staff:
            return queryset.all()

        return queryset.published()


class ProjectFeaturedViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for featured projects.
    - Public/Admin: Read-only access.
    """

    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"

    @method_decorator(cache_page(settings.CACHE_TIMEOUT))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(settings.CACHE_TIMEOUT))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == "list":
            return ProjectListSerializer
        return ProjectSerializer

    def get_queryset(self):
        queryset = Project.objects.prefetch_related("technologies")
        if self.request.user.is_staff:
            return queryset.all()

        return queryset.published().featured()
