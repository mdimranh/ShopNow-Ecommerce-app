from django.contrib.auth.models import User
from django.db.models.signals import post_init
from django.dispatch import receiver
from .models import UserProfile

@receiver(post_init, sender = User)
def create_user_profile(sender, instance, **kwargs):
    UserProfile.objects.create(user = instance)