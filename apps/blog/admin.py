from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Admin interface for the Post model.
    """

    list_display = ("title", "author", "status", "created_at")
    list_filter = ("status", "author", "created_at")
    search_fields = ("title", "summary", "content")
    ordering = ("-created_at",)
    prepopulated_fields = {"slug": ("title",)}

    fieldsets = (
        (None, {"fields": ("title", "slug", "author", "summary", "content")}),
        ("Status", {"fields": ("status",)}),
        ("Media", {"fields": ("image",)}),
    )
