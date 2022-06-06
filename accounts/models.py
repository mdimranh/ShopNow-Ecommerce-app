from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from datetime import datetime
import hashlib

from region.models import *


class EmailConfirmed(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    activation_key = models.CharField(max_length=500)
    email_confirmd = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name_plural = 'User email confirmed'

@receiver(pre_save, sender=User)
def email_as_username(sender, instance, *args, **kwargs):
    instance.username = instance.email

@receiver(post_save, sender=User)
def create_user_email_confirmation(sender, instance, created, **kwargs):
    if created:
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        email_confirmed_instance = EmailConfirmed(user = instance)
        user_encoded = f'{instance.email}-{date}'.encode()
        activation_key = hashlib.sha224(user_encoded).hexdigest()
        email_confirmed_instance.activation_key = activation_key
        email_confirmed_instance.save()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name="profile_info")
    phone = models.CharField(max_length=20)
    birthday = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    image = models.ImageField(upload_to = 'user/', blank=True)

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
    
