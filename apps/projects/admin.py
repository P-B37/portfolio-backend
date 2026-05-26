from django.contrib import admin

from .models import Project, Technology


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "slug", "icon_name")
    list_filter = ("category",)
    search_fields = ("name", "category")
    prepopulated_fields = {"slug": ("name",)}


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
    filter_horizontal = ("technologies",)

    fieldsets = (
        (None, {"fields": ("title", "slug", "summary", "content")}),
        ("Technologies", {"fields": ("technologies",)}),
        ("URLs", {"fields": ("repository_url", "live_demo_url")}),
        ("Status", {"fields": ("status", "is_featured")}),
        ("Media", {"fields": ("image",)}),
    )
