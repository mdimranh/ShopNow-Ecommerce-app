from django.contrib import admin
from django.contrib.auth.models import Group

from .models import UserProfile, AddressBook, EmailConfirmed

# admin.site.unregister(Group)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone',]
admin.site.register(UserProfile, ProfileAdmin)
admin.site.register(AddressBook)
admin.site.register(EmailConfirmed)
