from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Profile

admin.site.unregister(Group)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'address', 'image_tag']
admin.site.register(Profile, ProfileAdmin)