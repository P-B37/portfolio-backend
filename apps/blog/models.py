import uuid

from django.conf import settings
from django.core.validators import MaxLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

# hexagonal/Ports: import shared mixins
from apps.core.models import SoftDeleteModel, TimeStampedModel

from .managers import PostManager


class StatusChoices(models.TextChoices):
    DRAFT = "DF", _("Draft")
    PUBLISHED = "PB", _("Published")
    ARCHIVED = "AC", _("Archived")


class Category(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify

            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify

            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(TimeStampedModel, SoftDeleteModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blog_posts",
        verbose_name=_("Author"),
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
        verbose_name=_("Category"),
    )

    tags = models.ManyToManyField(
        Tag,
        related_name="posts",
        blank=True,
        verbose_name=_("Tags"),
    )

    title = models.CharField(max_length=255, verbose_name=_("Title"))
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    summary = models.TextField(
        help_text="Short overview of the article",
        validators=[MaxLengthValidator(500)],
    )
    content = models.TextField(
        help_text="Main content of the blog post in markdown format"
    )
    reading_time = models.PositiveIntegerField(
        help_text="Estimated reading time in minutes",
        null=True,
        blank=True,
    )

    image = models.ImageField(upload_to="portfolio/", null=True, blank=True)

    status = models.CharField(
        max_length=2,
        choices=StatusChoices.choices,
        default=StatusChoices.DRAFT,
        verbose_name=_("Status"),
    )

    views_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of page views",
        verbose_name=_("Views Count"),
    )
    likes_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of post claps/likes",
        verbose_name=_("Likes Count"),
    )

    objects = PostManager()

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")

        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["slug"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return self.title
