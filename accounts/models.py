from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

from region.models import *

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name="profile_info")
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=300, blank=True)
    city = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to = 'user/', blank=True)
    online = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def name(self):
        return self.user.first_name+" "+self.user.last_name

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="{}" height="50" weight="50" />'.format(self.image.url))
    image_tag.short_description = 'Image'

    class Meta:
        verbose_name_plural = 'Profiles'
        app_label = 'auth'


class AddressBook(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name="address_book")
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    country = models.ForeignKey(Country, on_delete = models.CASCADE, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete = models.CASCADE, blank=True, null=True)
    city = models.ForeignKey(City, on_delete = models.CASCADE, blank=True, null=True)
    area = models.ForeignKey(Area, on_delete = models.CASCADE, blank=True, null=True)
    address = models.CharField(max_length=500)
    default = models.BooleanField(default=True)
    temp = models.BooleanField(default=False)

    def __str__(self):
        return self.name+" ("+self.user.first_name+" "+self.user.last_name+")"
    
