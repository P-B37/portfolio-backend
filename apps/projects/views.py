from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.db.models import F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

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

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["category__slug", "category__name"]
    search_fields = ["title", "summary", "content"]
    ordering_fields = [
        "created_at",
        "claps_count",
    ]

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
        queryset = Project.objects.select_related("category").prefetch_related("technologies")
        if self.request.user.is_staff:
            return queryset.all()

        return queryset.published()

    @action(detail=True, methods=["POST"], permission_classes=[AllowAny])
    def clap(self, request, slug=None):
        project = self.get_object()
        amount = request.data.get("amount", 1)

        try:
            amount = int(amount)
            if amount < 1 or amount > 50:
                return Response(
                    {"error": "Clap amount must be between 1 and 50."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except (ValueError, TypeError):
            return Response(
                {"error": "Invalid clap amount."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Clear cache to guarantee listing endpoints reflect real-time count
        from django.core.cache import cache
        cache.clear()

        project.claps_count = F("claps_count") + amount
        project.save(update_fields=["claps_count"])

        project.refresh_from_db()
        return Response({"claps_count": project.claps_count}, status=status.HTTP_200_OK)


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
        queryset = Project.objects.select_related("category").prefetch_related("technologies")
        if self.request.user.is_staff:
            return queryset.all()

        return queryset.published().featured()
