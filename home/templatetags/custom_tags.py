from django import template
from order.models import ShopCart
from product.models import Category, Subcategory, Group
from setting.models import Menus

from django.contrib.auth.admin import User

register = template.Library()

@register.simple_tag
def Cart(value):
    if User.objects.get(id = value).is_authenticated:
        shopcart = ShopCart.objects.filter(user__id = value, on_order=False)
        total_cost = 0
        for item in shopcart:
            price = item.product.main_price - (item.product.main_price * item.product.discount / 100)
            cost = price*item.quantity
            total_cost += cost
        for item in shopcart[:1]:
            if item.coupon:
                if item.coupon.discount_type == 'fixed':
                    total_cost -= item.coupon.value
                else:
                    total_cost = total_cost - (total_cost * item.coupon.value / 100)
    return [shopcart, total_cost]
register.filter('shopcart', Cart)

@register.filter
def Categorys(value):
    return Category.objects.all()
register.filter('categorys', Categorys)

@register.filter(name="menus")
def Menu(value):
    return Menus.objects.all().exclude(active=False).order_by('position')


