from django.contrib.auth.models import User
from django.db.models.signals import post_init
from django.dispatch import receiver
from .models import Profile

@receiver(post_init, sender = User)
def create_user_profile(sender, instance, **kwargs):
    Profile.objects.create(user = instance)