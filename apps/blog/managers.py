from django.db import models


class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status="PB")

    def by_author(self, author):
        return self.filter(author=author)


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db).filter(is_deleted=False)

    def published(self):
        return self.get_queryset().published()

    def by_author(self, author):
        return self.get_queryset().by_author(author)
