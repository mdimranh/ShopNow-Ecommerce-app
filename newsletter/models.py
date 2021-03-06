from django.db import models
from ckeditor.fields import RichTextField
from django.utils.timezone import now
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.postgres.fields import ArrayField

class NewsletterEmail(models.Model):
    email = models.EmailField()
    active = models.BooleanField(default=True)
    


class Newsletter(models.Model):
    emails = ArrayField(
        ArrayField(
            models.EmailField(blank=True), null=True
        ), null=True
    )
    subject = models.TextField()
    body = RichTextField()
    send_date = models.DateTimeField(default=now)

    def total_email(self):
        return len(self.emails)
