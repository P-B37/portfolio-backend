from django.contrib import admin

from .models import Category, Project, Technology


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


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

    list_display = ("title", "category", "status", "is_featured", "created_at")
    list_filter = ("category", "status", "is_featured", "created_at")
    search_fields = ("title", "summary", "content")
    ordering = ("-created_at",)
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("technologies",)

    fieldsets = (
        (None, {"fields": ("title", "slug", "category", "summary", "content")}),
        ("Technologies", {"fields": ("technologies",)}),
        ("URLs", {"fields": ("repository_url", "live_demo_url")}),
        ("Status", {"fields": ("status", "is_featured")}),
        ("Media", {"fields": ("image",)}),
    )
