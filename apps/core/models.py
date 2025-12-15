from django.db import models
from django.utils import timezone

class SoftDeleteManager(models.Manager):
    """Custom manager for SoftDeleteModel.

    Provides methods to filter out or include soft-deleted objects in querysets.
    """
    def get_queryset(self):
        """
        Returns a queryset containing only non-deleted objects.
        """
        return super().get_queryset().filter(is_deleted=False)
    
    def all_with_deleted(self):
        """
        Returns a queryset of all objects, including soft-deleted ones.
        """
        return super().get_queryset()

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