from django.contrib import admin

from .models import *


from solo.admin import SingletonModelAdmin
from .models import SiteConfiguration, SiteFront

admin.site.register(SiteConfiguration, SingletonModelAdmin)
admin.site.register(SiteFront, SingletonModelAdmin)


# shopinfo = ShopInfo.objects.all().first()
admin.site.site_header = str(SiteConfiguration.name)+" "+"Administration"

class SliderSettingInline(admin.TabularInline):
    model = SliderSetting

    class Media:
        css = {'all': ('no-delete.css',)}

class SlideInline(admin.TabularInline):
    model = Slide
    readonly_fields = ['image_tag']
    extra = 0

class SliderAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_per_page = 10
    inlines = [SliderSettingInline, SlideInline]
admin.site.register(Slider, SliderAdmin)

class BannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'banner_type', 'active', 'image_tag']
    list_per_page = 10
admin.site.register(Banner, BannerAdmin)

class TeamInfoInline(admin.TabularInline):
    model = TeamInfo
    readonly_fields = ['image_tag']
    extra = 3

class AboutusAdmin(admin.ModelAdmin):
    list_display = ['line1', 'image_tag']
    inlines = [TeamInfoInline]
admin.site.register(Aboutus, AboutusAdmin)

# class TeamInfoAdmin(admin.ModelAdmin):
#     list_display = ['name', 'job_title', 'image_tag']
# admin.site.register(TeamInfo, TeamInfoAdmin)

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'message', 'note']
    list_filter = ['status', 'created_at', 'updated_at']
admin.site.register(ContactMessage, ContactMessageAdmin)

admin.site.register(Region)
