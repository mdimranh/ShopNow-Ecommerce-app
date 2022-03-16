from django.contrib import admin

from .models import *

class ShopCartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'created_at', 'product_image', 'coupon_active']
admin.site.register(ShopCart, ShopCartAdmin)

class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'created_at', 'product_image']
admin.site.register(Wishlist, WishlistAdmin)

class UserRestrictionInlin(admin.TabularInline):
    model = UserRestrictions
    extra = 1
    max_num = 1

class UserLimitsInlin(admin.TabularInline):
    model = UserLimits
    extra = 1
    max_num = 1

class CouponAdmin(admin.ModelAdmin):
    list_display = ['name', 'discount_type', 'value', 'active']
    list_filter = ['discount_type', 'start_date', 'end_date', 'active']
    inlines = [UserRestrictionInlin, UserLimitsInlin]

admin.site.register(Coupon, CouponAdmin)
admin.site.register(Order)
admin.site.register(ShippingMethod)
