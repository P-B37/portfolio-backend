from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, ProjectFeaturedViewSet

app_name = "projects"

router = DefaultRouter()
router.register(r"featured", ProjectFeaturedViewSet, basename="featured-projects")
router.register(r"", ProjectViewSet, basename="projects")

urlpatterns = router.urls
