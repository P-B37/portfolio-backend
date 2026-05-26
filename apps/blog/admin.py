from django.contrib import admin

from .models import Category, Post, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Admin interface for the Post model.
    """

    list_display = (
        "title",
        "category",
        "author",
        "status",
        "views_count",
        "likes_count",
        "created_at",
    )
    list_filter = ("status", "category", "author", "created_at")
    search_fields = ("title", "summary", "content")
    ordering = ("-created_at",)
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags",)
    readonly_fields = ("views_count", "likes_count")

    fieldsets = (
        (None, {"fields": ("title", "slug", "author", "summary", "content")}),
        ("Taxonomy", {"fields": ("category", "tags")}),
        ("Status & Engagement", {"fields": ("status", "views_count", "likes_count")}),
        ("Media", {"fields": ("image",)}),
    )
