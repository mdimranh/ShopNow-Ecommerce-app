from django.contrib import admin

from .models import ShopCart

class ShopCartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'product_image']
admin.site.register(ShopCart, ShopCartAdmin)
