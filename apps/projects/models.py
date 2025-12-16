import uuid
from django.db import models
from django.core.validators import MaxLengthValidator
from django.utils.translation import gettext_lazy as _

from core.models import SoftDeleteModel, TimeStampedModel
from .manager import ProjectManager


class Status(models.TextChoices):
    DRAFT = "DR", _("Draft")
    PUBLISHED = "PB", _("Published")
    ARCHIVED = "AR", _("Archived")


class Project(SoftDeleteModel, TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    summary = models.TextField(
        help_text="Short overview for cards.",
        validators=[MaxLengthValidator(500)],
    )
    content = models.TextField(help_text="Markdown supported")

    image = models.ImageField(upload_to="portfolio/", null=True, blank=True)

    repository_url = models.URLField(null=True, blank=True)
    live_demo_url = models.URLField(null=True, blank=True)

    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    is_featured = models.BooleanField(default=False)
    objects = ProjectManager()

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Project"
        verbose_name_plural = "Projects"

        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["is_featured"]),
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return self.title
