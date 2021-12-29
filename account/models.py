from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=300, blank=True)
    city = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to = 'user/', blank=True)

    def __str__(self):
        return self.user.username

    def name(self):
        return self.user.first_name+" "+self.user.last_name

    def image_tag(self):
        return mark_safe('<img src="{}" height="50" weight="50" />'.format(self.image.url))
    image_tag.short_description = 'Image'

    class Meta:
        verbose_name_plural = 'Profiles'
        app_label = 'auth'
