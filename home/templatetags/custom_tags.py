from django import template
from order.models import ShopCart
from product.models import Category, Subcategory, Group
from setting.models import Menus, Currency, Settings

from django.contrib.auth.admin import User

register = template.Library()

@register.simple_tag
def Cart(value):
    if User.objects.get(id = value).is_authenticated:
        scart, create = ShopCart.objects.get_or_create(user__id = value, on_order=False)
        total_cost = 0
        cart_serialize = []
        cs={}
        for cart in scart.carts.all():
            price = cart.product.main_price - (cart.product.main_price * cart.product.discount / 100)
            cost = price*cart.quantity
            total_cost += cost
        # if scart.coupon.all().count() > 0:
        #     cpn_dis = 0
        #     for cpn in scart.coupon.all():
        #         cpn_dis += cpn.value if cpn.discount_type.lower() == 'fixed' else total_cost * cpn.value / 100
        #     total_cost -= cpn_dis
    return [scart, total_cost]
register.filter('shopcart', Cart)

@register.filter
def Categorys(value):
    return Category.objects.all()
register.filter('categorys', Categorys)

@register.filter(name="menus")
def Menu(value):
    return Menus.objects.all().exclude(active=False).order_by('position')

@register.simple_tag
def currencies():
    cur = Currency.objects.all().values_list('code', flat=True)
    return cur
# register.filter('currencies', Currencies)

@register.simple_tag
def DefaultCurrency():
    return Settings.objects.all().first().default_currency.code

# @register.simple_tag(takes_context=True)
# def mycurrency(context):
#     currency = context['request'].COOKIES['currency']
#     get_currency = Currency.objects.get(code = currency)
#     return [currency, get_currency.rate, get_currency.symbol_native]

@register.simple_tag(takes_context=True)
def mycurrency(context):
    try:
        get_currency = Currency.objects.get(code = context['request'].COOKIES['mycurrency'])
        exists = True
    except:
        get_currency = Settings.objects.filter().first().default_currency
        exists = False
    return [get_currency.rate, get_currency.symbol_native, exists]

