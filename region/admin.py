from django.contrib import admin

from .models import *

class CountryInline(admin.TabularInline):
    model = Country
    extra = 1

class RegionAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [CountryInline]
admin.site.register(Regions, RegionAdmin)

class StateInline(admin.TabularInline):
    model = State
    extra = 1

class CountryAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [StateInline]
admin.site.register(Country, CountryAdmin)

class CityInline(admin.TabularInline):
    model = City
    extra = 1

class StateAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [CityInline]
admin.site.register(State, StateAdmin)

class AreaInline(admin.TabularInline):
    model = Area
    extra = 1

class CityAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [AreaInline]
admin.site.register(City, CityAdmin)
admin.site.register(Area)
