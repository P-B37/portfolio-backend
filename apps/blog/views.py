from django.conf import settings
from django.db.models import F
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

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
    filterset_fields = ["category__slug", "category__name"]
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

    @action(detail=True, methods=["post"], permission_classes=[AllowAny])
    def like(self, request, slug=None):
        instance = self.get_object()
        
        # Prevent multiple likes from the same visitor session
        liked_posts = request.session.get("liked_posts", [])
        if instance.slug in liked_posts:
            return Response({
                "likes_count": instance.likes_count,
                "already_liked": True,
                "error": "You have already liked this post."
            }, status=200)

        # Standardize increment to exactly +1 since one user can only like once
        Post.objects.filter(pk=instance.pk).update(likes_count=F("likes_count") + 1)
        
        # Match in-memory representation
        instance.likes_count += 1
        
        # Save to session list
        liked_posts.append(instance.slug)
        request.session["liked_posts"] = liked_posts
        request.session.modified = True
        
        return Response({
            "likes_count": instance.likes_count,
            "already_liked": False
        })

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
