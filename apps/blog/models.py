import uuid
from django.db import models
from django.conf import settings
from django.core.validators import MaxLengthValidator
from django.utils.translation import gettext_lazy as _

# hexagonal/Ports: import shared mixins
from apps.core.models import TimeStampedModel, SoftDeleteModel
from .managers import PostManager


class StatusChoices(models.TextChoices):
    DRAFT = "DF", _("Draft")
    PUBLISHED = "PB", _("Published")
    ARCHIVED = "AC", _("Archived")


class Post(TimeStampedModel, SoftDeleteModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blog_posts",
        verbose_name=_("Author"),
    )

    title = models.CharField(max_length=255, verbose_name=_("Title"))
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    summary = models.TextField(
        help_text="Short overview of the article",
        validators=[MaxLengthValidator(500)],
    )
    content = models.TextField(
        help_text="Main content of the blog\
            post in markdown format"
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

    objects = PostManager()

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")

        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return self.title
