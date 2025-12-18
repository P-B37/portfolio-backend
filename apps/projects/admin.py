from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    Admin interface for the Project model.
    """

    list_display = ("title", "status", "is_featured", "created_at")
    list_filter = ("status", "is_featured", "created_at")
    search_fields = ("title", "summary", "content")
    ordering = ("-created_at",)
    prepopulated_fields = {"slug": ("title",)}

    fieldsets = (
        (None, {"fields": ("title", "slug", "summary", "content")}),
        ("URLs", {"fields": ("repository_url", "live_demo_url")}),
        ("Status", {"fields": ("status", "is_featured")}),
        ("Media", {"fields": ("image",)}),
    )
