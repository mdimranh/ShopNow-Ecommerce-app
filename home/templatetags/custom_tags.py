from django import template
from django.db.models import Q
from order.models import ShopCart, ShippingMethod, Wishlist
from product.models import Category, Subcategory, Group
from setting.models import Menus, Currency, Settings, FooterLinks

from django.conf import settings
import os

import base64
from django.contrib.staticfiles.finders import find as find_static_file

from order.cartdetails import cartDetails

from django.contrib.auth.admin import User

register = template.Library()

@register.simple_tag(takes_context=True)
def wishlist(context):
	request = context.get("request")
	device = request.COOKIES['device']
	if request.user.is_authenticated:
		user = request.user
		if Wishlist.objects.filter(Q(device = device) | Q(user = user)).exists():
			wlist = Wishlist.objects.get(Q(device = device) | Q(user = user))
		else:
			wlist = Wishlist(
				user=user,
				device=device
			)
			wlist.save()
	else:
		if Wishlist.objects.filter(device = device).exists():
			wlist = Wishlist.objects.get(device = device)
		else:
			wlist = Wishlist(
				device=device
			)
			wlist.save()
	pro_list = []
	for pro in wlist.product.all():
		pro_list.append(pro)
	return [wlist, pro_list]

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
	currency = Settings.objects.all().first().default_currency
	return [currency.code, currency.rate, currency.symbol_native]

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

@register.filter
def FLinks(value):
	link_list = FooterLinks.objects.filter(section_name=value).first().links.all()
	return link_list
register.filter('footerlink', FLinks)


@register.simple_tag(takes_context=True)
def cart(context):
	request = context.get("request")
	device = request.COOKIES['device']
	if request.user.is_authenticated:
		ucart, create = ShopCart.objects.get_or_create(user=request.user, on_order=False)
	gcart, create = ShopCart.objects.get_or_create(device=device, on_order=False)
	if request.COOKIES.get('cart'):
		cart_type = request.COOKIES['cart']
		if cart_type == 'ucart' and request.user.is_authenticated:
			cart = ucart
			title = 'User Cart'
			type = 'gcart'
			type_text = 'GuestCart'
			mergefrom = 'gcart'
			mergefrom_text = 'Merge GuestCart'
			mergefrom_size = gcart.carts.all().count()
		else:
			cart = gcart
			title = 'Guest Cart'
			type = 'ucart'
			type_text = 'UserCart'
			mergefrom = 'ucart'
			mergefrom_text = 'Merge UserCart'
			if request.user.is_authenticated:
				mergefrom_size = ucart.carts.all().count()
			else:
				mergefrom_size = 0
	else:
		if ucart.carts.all().count() >= gcart.carts.all().count():
			cart = ucart
			title = 'User Cart'
			type = 'gcart'
			type_text = 'GuestCart'
			mergefrom = 'gcart'
			mergefrom_text = 'Merge GuestCart'
		else:
			cart = gcart
			title = 'Guest Cart'
			type = 'ucart'
			type_text = 'UserCart'
			mergefrom = 'ucart'
			mergefrom_text = 'Merge UserCart'

	mycart = cartDetails(cart)

	return {
		"cart": cart,
		"title": title,
		'type': type,
		'type_text': type_text,
		'mergefrom': mergefrom,
		'mergefrom_text': mergefrom_text,
		'mergefrom_size': mergefrom_size,
		'subtotal': mycart.subtotal,
		'total_cost': (mycart.subtotal - mycart.coupon_discount) + mycart.ship_cost,
		'ship': True,
		'ship_name': mycart.ship_name,
		'ship_cost': mycart.ship_cost
	}

@register.filter
def intformat(value, length):
	if len(str(value)) < length:
		no_zero = length - len(str(value))
		return '0'*no_zero+str(value)
	else:
		return value
register.filter('intformat', intformat)

