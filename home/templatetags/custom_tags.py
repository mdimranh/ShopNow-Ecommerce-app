from django import template
from django.db.models import Q
from order.models import ShopCart, ShippingMethod
from product.models import Category, Subcategory, Group
from setting.models import Menus, Currency, Settings, FooterLinks

from django.contrib.auth.admin import User

register = template.Library()

@register.simple_tag(takes_context=True)
def shopcart(context):
	request = context.get("request")
	device = request.COOKIES['device']
	ucart, create = ShopCart.objects.get_or_create(user=request.user, on_order=False)
	gcart, create = ShopCart.objects.get_or_create(device=device, on_order=False)
	if request.COOKIES.get('cart'):
		cart_type = request.COOKIES['cart']
		if cart_type == 'ucart':
			cart = ucart
		else:
			cart = gcart
	else:
		if ucart.carts.all().count() >= gcart.carts.all().count():
			cart = ucart
		else:
			cart = gcart

	total_cost = 0
	for item in cart.carts.all():
		price = item.product.main_price - (item.product.main_price * item.product.discount / 100)
		cost = price*item.quantity
		total_cost += cost
	
	return [cart, total_cost]

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

	total_cost = 0
	subtotal = 0
	for item in cart.carts.all():
		print("option-------->", item.options)
		price = item.product.main_price - (item.product.main_price * item.product.discount / 100)
		cost = price*item.quantity
		total_cost += cost
		subtotal = total_cost
	
	free_ship = False
	if cart.coupon.all().count() > 0:
		for coupon in cart.coupon.all():
			if coupon.discount_type == 'Percent':
				total_cost_with_coupon = total_cost - total_cost*coupon.value/100
			else:
				total_cost_with_coupon = total_cost - coupon.value
			if coupon.free_shipping:
				free_ship = True
		total_cost = total_cost_with_coupon
	
	free_shipping = ShippingMethod.objects.filter(method_type='free').first()
	local_shipping = ShippingMethod.objects.filter(method_type='local').first()
	ship = True
	if free_ship:
		if free_shipping.active:
			ship_name = free_shipping.name
			ship_cost = 0
		else:
			ship_name = 'Free Shipping'
			ship_cost = 0
	else:
		if free_shipping and free_shipping.active and total_cost > free_shipping.fee:
			ship_name = free_shipping.name
			ship_cost = 0
		elif local_shipping and local_shipping.active:
			ship_name = local_shipping.name
			ship_cost = local_shipping.fee
			total_cost += local_shipping.fee
		else:
			ship = False
			ship_name = ''
			ship_cost = ''

	return {
		"cart": cart,
		"title": title,
		'type': type,
		'type_text': type_text,
		'mergefrom': mergefrom,
		'mergefrom_text': mergefrom_text,
		'mergefrom_size': mergefrom_size,
		'subtotal': subtotal,
		'total_cost': total_cost,
		'ship': ship,
		'ship_name': ship_name,
		'ship_cost': ship_cost
	}

