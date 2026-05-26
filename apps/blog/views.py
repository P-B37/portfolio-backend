from django.conf import settings
from django.db.models import F
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.response import Response

from apps.core.pagination import CustomPagination
from apps.core.permissions import IsAdminOrReadOnly

from .models import Post
from .serializers import BlogPostListSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):

    pagination_class = CustomPagination
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["title", "summary", "content"]
    ordering_fields = [
        "created_at",
        "reading_time",
        "views_count",
        "likes_count",
    ]

    @method_decorator(cache_page(settings.CACHE_TIMEOUT))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        # Dynamically increment views count on retrieve safely without race conditions
        instance = self.get_object()
        Post.objects.filter(pk=instance.pk).update(views_count=F("views_count") + 1)

        # Match in-memory representation so that the serializer return value is accurate
        # and we completely save another database hit from super().retrieve()
        instance.views_count += 1
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == "list":
            return BlogPostListSerializer
        return PostSerializer

    def get_queryset(self):
        queryset = Post.objects.select_related("author", "category").prefetch_related(
            "tags"
        )

        if self.request.user.is_staff:
            return queryset.all()
        return queryset.published()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
