from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Project
from .services import generate_project_slug


@receiver(pre_save, sender=Project)
def set_project_slug(sender, instance: Project, **kwargs):
    """
    Signal receiver to set a unique slug for a Project instance before saving.

    This function generates a slug based on the project's title and ID,
    ensuring that each project has a unique and SEO-friendly identifier.

    Args:
        sender (Model): The model class sending the signal (Project).
        instance (Project): The instance of the Project being saved.
    """
    if not instance.slug:
        instance.slug = generate_project_slug(instance.title, instance.id)
