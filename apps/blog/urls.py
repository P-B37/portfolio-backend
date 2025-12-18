from rest_framework.routers import DefaultRouter
from .views import PostViewSet

app_name = "blog"

router = DefaultRouter()
router.register(r"", PostViewSet, basename="post")

urlpatterns = router.urls
