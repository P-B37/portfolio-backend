from core.models import TimeStampedModel
from django.db import models


class ContactMessage(TimeStampedModel):
    """
    Model to store incoming messages from the contact form.
    Provides a secure backup in case of email delivery failure.
    """

    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"{self.subject} - from {self.name} ({self.email})"
