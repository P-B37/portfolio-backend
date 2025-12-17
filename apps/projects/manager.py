from django.db import models
from django.db.models.query import QuerySet


class ProjectQuerySet(QuerySet):
    """
    Custom QuerySet for the Project model.
    """

    def published(self):
        """
        Returns only published projects.
        """
        return self.filter(status="PB")

    def featured(self):
        """
        Returns only featured projects.
        """
        return self.filter(is_featured=True)


class ProjectManager(models.Manager):
    """
    Custom manager for the Project model.
    """

    def get_queryset(self):
        """
        Returns the custom ProjectQuerySet,
        excluding deleted projects.
        """
        return ProjectQuerySet(self.model, using=self._db).filter(is_deleted=False)

    def published(self):
        """
        Returns published projects.
        """
        return self.get_queryset().published()

    def featured(self):
        """
        Returns featured projects.
        """
        return self.get_queryset().featured()
