from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Post
from .services import calculate_reading_time, generate_blog_slug


@receiver(pre_save, sender=Post)
def pre_save_post_receiver(sender, instance, **kwargs):
    """
    Signal to automatically generate slug and calculate reading time
    before saving a Post instance.
    """
    if not instance.slug:
        instance.slug = generate_blog_slug(instance.title)

    if instance.content:
        instance.reading_time = calculate_reading_time(instance.content)
