from django.db import models
from django.utils import timezone

from .managers import SoftDeleteManager


class SoftDeleteModel(models.Model):
    """Abstract model for soft deletion.

    Instead of permanently deleting a record from the database, this model
    marks it as deleted by setting `is_deleted` to True and recording the
    deletion time in `deleted_at`.

    It provides `delete()` and `restore()` methods to manage the soft
    deletion status. The `hard_delete()` method can be used to permanently
    delete the record.
    """

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        """
        Soft deletes the object.

        Sets the is_deleted flag to True and records the deletion time.
        """
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        """
        Restores a soft-deleted object.

        Sets the is_deleted flag to False and clears the deleted_at field.
        """
        self.is_deleted = False
        self.deleted_at = None
        self.save()

    def hard_delete(self):
        """
        Permanently deletes the object from the database.
        """
        super().delete()


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
