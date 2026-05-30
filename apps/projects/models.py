import uuid

from core.models import SoftDeleteModel, TimeStampedModel
from django.core.validators import MaxLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .manager import ProjectManager


class Status(models.TextChoices):
    DRAFT = "DR", _("Draft")
    PUBLISHED = "PB", _("Published")
    ARCHIVED = "AR", _("Archived")


class Category(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify

            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Technology(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    icon_name = models.CharField(
        max_length=50,
        blank=True,
        help_text="Lucide or DevIcon class name (e.g., 'cisco', 'python', 'ansible')",
    )
    category = models.CharField(
        max_length=50,
        blank=True,
        help_text="e.g., Automation, Networking, Development, DevOps, Cloud",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Technology"
        verbose_name_plural = "Technologies"

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify

            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Project(SoftDeleteModel, TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    summary = models.TextField(
        help_text="Short overview for the project",
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
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="projects",
        verbose_name=_("Category"),
    )

    is_featured = models.BooleanField(default=False)
    claps_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of project claps",
        verbose_name=_("Claps Count"),
    )
    technologies = models.ManyToManyField(
        Technology,
        related_name="projects",
        blank=True,
        help_text="Selected technology tags for this project",
    )
    objects = ProjectManager()

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Project"
        verbose_name_plural = "Projects"

        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["is_featured"]),
            models.Index(fields=["slug"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return self.title
