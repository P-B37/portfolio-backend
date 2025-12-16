from django.db import models

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