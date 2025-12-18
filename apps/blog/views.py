from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from apps.core.permissions import IsAdminOrReadOnly
from apps.core.pagination import CustomPagination
from .models import Post
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):

    serializer_class = PostSerializer
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
    ]

    def get_queryset(self):
        queryset = Post.objects.select_related("author")

        if self.request.user.is_staff:
            return queryset.all()
        return queryset.published()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
