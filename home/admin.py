from django.contrib import admin

from .models import *

admin.site.register(ShopInfo)


class SlidingAdmin(admin.ModelAdmin):
    list_display = ['line_1', 'line_2', 'line_3', 'active', 'image_tag']
    list_per_page = 10
    search_fields = ['line_1', 'line_2', 'line_3']
admin.site.register(Sliding, SlidingAdmin)

class BannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'big_banner', 'active', 'image_tag']
    list_per_page = 10
admin.site.register(Banner, BannerAdmin)

class AboutusAdmin(admin.ModelAdmin):
    list_display = ['line1', 'image_tag']
admin.site.register(Aboutus, AboutusAdmin)

class TeamInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'job_title', 'image_tag']
admin.site.register(TeamInfo, TeamInfoAdmin)

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'message', 'note']
    list_filter = ['status', 'created_at', 'updated_at']
admin.site.register(ContactMessage, ContactMessageAdmin)