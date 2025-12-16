from django.db import models
from django.db.models.query import QuerySet


class ProjectQuerySet(QuerySet):
    def published(self):
        return self.filter(status="PB")

    def featured(self):
        return self.filter(is_featured=True)


class ProjectManager(models.Manager):
    def get_queryset(self):
        return ProjectQuerySet(self.model, using=self._db).filter(is_deleted=False)

    def published(self):
        return self.get_queryset().published()

    def featured(self):
        return self.get_queryset().featured()
