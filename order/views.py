from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from django.views.generic import TemplateView
from django.views import View

from django.contrib.auth.models import User
from django.contrib import messages

from django.db.models import Q

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site

# from setting.models import EmailConfig
from control.emailconfig import backend

from setting.models import Currency

from .models import ShopCart, Coupon, Wishlist
from setting.models import Currency
from product.models import Product, Option, Category
from region.models import Country, Region, City, Area
from order.models import ShippingMethod, PaymentMethod, Order, Cart
from accounts.models import AddressBook
from .cartdetails import cartDetails

import json

class AddToCart(View):
	def post(self, request):
		if 'update-quantity' in request.POST:
			getcart = Cart.objects.get(id = request.POST['id'])
			if getcart.product.amount < int(request.POST["update-quantity"]):
				s = 's' if getcart.product.amount > 1 else ''
				msg = f"We have only {getcart.product.amount} product{s}"
				msg_type = 'fail'
				return JsonResponse({'msg':msg, 'msg_type':msg_type})
			else:
				getcart.quantity = request.POST['update-quantity']
				getcart.save()
				scart = ShopCart.objects.get(user = request.user, on_order=False)
				total_cost = 0
				cart_serialize = []
				cs={}
				subtotal = 0
				for cart in scart.carts.all():
					price = cart.product.main_price - (cart.product.main_price * cart.product.discount / 100)
					cost = price*cart.quantity
					total_cost += cost
					subtotal = total_cost
					cs = {
						"id": cart.id,
						"category": cart.product.category.name,
						"title": cart.product.title,
						"image": cart.product.image,
						"main_price": str(cart.product.main_price),
						"price": str(cart.product.main_price - (cart.product.main_price * cart.product.discount / 100)),
						"discount": str(cart.product.discount),
						"amount": cart.quantity
					}
					cart_serialize.append(cs)
				
				cart = cartDetails(scart)
				msg = "Product successfully added to cart!"
				return JsonResponse({'msg_type':'success', 'item':scart.carts.all().count(), 'cost':cart.subtotal, 'subtotal': cart.subtotal, 'msg': msg, 'cart': cart_serialize})
		else:
			cart_type = request.COOKIES['cart']
			if cart_type == 'ucart':
				scart = ShopCart.objects.get(user = request.user, on_order = False)
			else:
				scart = ShopCart.objects.get(device = request.COOKIES['device'], on_order = False)
			pro_id = int(request.POST['id'])
			if Product.objects.filter(id = pro_id).exists():
				pro_list = list(scart.carts.values_list('product__id', flat=True))
				if pro_id in pro_list:
					return JsonResponse({'msg_type':'fail', 'msg': "Product already exist to your cart."})
				pro = Product.objects.get(id = pro_id)
				if pro.amount < 0:
					return JsonResponse({'msg_type':'fail', 'msg': "Out of stock"})
				else:
					try:
						color = request.POST['color']
					except:
						color = None
					try:
						size = request.POST['size']
					except:
						size = None
					cart = Cart(
						product= pro,
						quantity = request.POST['quantity'],
						color=color,
						size=size
					)
					cart.save()
					for opt_id in request.POST.getlist('options[]'):
						option = Option.objects.get(id = opt_id)
						cart.options.add(option)
					scart.carts.add(cart)
					scart.save()
					try:
						Wishlist.objects.filter(product = pro, user = request.user).first().delete()
					except:
						pass
					cart_serialize = []
					cs={}
					for cart in scart.carts.all():
						cs = {
							"id": cart.id,
							"category": cart.product.category.name,
							"title": cart.product.title,
							"image": cart.product.image,
							"main_price": str(cart.product.main_price),
							"price": str(cart.product.main_price - (cart.product.main_price * cart.product.discount / 100)),
							"discount": str(cart.product.discount),
							"amount": cart.quantity
						}
						cart_serialize.append(cs)
					item = scart.carts.all().count()
					msg = "Product successfully added to cart!"
					mycart = cartDetails(scart)
					context = {
						'msg_type':'success',
						'item':item,
						'cost': mycart.subtotal - mycart.coupon_discount,
						'subtotal': mycart.subtotal,
						'msg': msg,
						'product': pro,
						'cart': cart_serialize
					}
					return JsonResponse(context)
			else:
				return JsonResponse({'msg': "Product is not exist."})

def CartView(request):
	if request.method == 'POST':
		getcart = Cart.objects.get(id = request.POST['cart-id'])
		if getcart.product.amount < int(request.POST["quantity"]):
			msg = f"We have only {getcart.product.amount} product"
			msg_type = 'quantity-update-fail'
			messages.error(request, msg, extra_tags=msg_type)
			return redirect(request.path_info)
		else:
			getcart.quantity = request.POST["quantity"]
			getcart.save()
			return redirect(request.path_info)

	return render(request, 'product/cart.html')

def CartDelete(request):
	getcart = Cart.objects.get(id = request.POST['id'])
	scart = getcart.shopcart_set.get()
	cart = cartDetails(scart)
	getcart.delete()
	msg = "Product successfully deleted"
	context = {
		'msg': msg
	}
	return JsonResponse(context)

def Checkout(request):
	if request.method == 'POST':
		if 'coupon-code' in request.POST:
			if Coupon.objects.filter(code = request.POST['coupon-code']).exists():
				cpn = Coupon.objects.get(code = request.POST['coupon-code'])
				if request.COOKIES['cart'] == 'ucart':
					scart = ShopCart.objects.get(user = request.user, on_order=False)
				else:
					scart = ShopCart.objects.get(device = request.COOKIES['device'], on_order=False)
				cost = 0
				total_cost = 0
				for cart in scart.carts.all():
					price = cart.product.main_price - (cart.product.main_price * cart.product.discount / 100)
					cost = price*cart.quantity
					total_cost += cost
				if scart.coupon.all().count() > 0:
					for coupon in cart.coupon.all():
						if coupon.discount_type == 'Percent':
							total_cost_with_coupon = total_cost - total_cost*coupon.value/100
						else:
							total_cost_with_coupon = total_cost - coupon.value
					total_cost = total_cost_with_coupon
					
				cpn_used = ShopCart.objects.filter(coupon=cpn).count()
				currency = Currency.objects.get(code = request.COOKIES['mycurrency'])
				if request.COOKIES['cart'] == 'ucart':
					my_used = ShopCart.objects.filter(user = request.user, coupon = cpn).count()
				else:
					my_used = ShopCart.objects.filter(device = request.COOKIES['device'], coupon = cpn).count()
				if cpn.limit_per_coupon != None and cpn_used >= cpn.limit_per_coupon:
					messages.error(request, 'This coupon have used maximum number of times..', extra_tags='cpn-error')
				elif cpn.limit_per_customer != None and my_used >= cpn.limit_per_customer:
					messages.error(request, 'You have used this coupon maximum number of times.', extra_tags='cpn-error')
				elif cpn.max_spend != None and total_cost >= cpn.max_spend:
					messages.error(request, f'This coupon is valid for maximum {currency.symbol_native}{cpn.max_spend*currency.rate}.', extra_tags='cpn-error')
				elif cpn.min_spend != None and total_cost <= cpn.min_spend:
					messages.error(request, f'This coupon is valid for minimum {currency.symbol_native}{cpn.max_spend*currency.rate}.', extra_tags='cpn-error')
				else:
					scart.coupon.add(cpn)
					return redirect(request.path_info)
				return redirect(request.path_info)
			else:
				messages.error(request, 'Invalid coupon code.', extra_tags='cpn-error')
				return redirect(request.path_info)
		else:
			scart = ShopCart.objects.get(id = request.POST['cartid'])
			cart = cartDetails(scart)
			if request.POST.get("diff-address") == 'on':
				country = Country.objects.get(id = request.POST['add-country']).name
				region = Region.objects.get(id = request.POST['add-region']).name
				city = City.objects.get(id = request.POST['add-city']).name
				area = Area.objects.get(id = request.POST['add-area']).name
				address = request.POST['address']
			else:
				address_book = AddressBook.objects.get(id = request.POST['address_book'])
				country = address_book.country.name
				region = address_book.region.name
				city = address_book.city.name
				area = address_book.area.name
				address = address_book.address
				
			scart = ShopCart.objects.get(id = request.POST['cartid'])
			first_name = request.POST['first_name']
			last_name = request.POST['last_name']
			email = request.POST['email']
			phone = request.POST['phone']
			try:
				payment_id = request.POST['payment_id']
				payment_mode = request.POST['payment_mode']
			except:
				payment_id = None
				payment_mode = 'cash'
			try:
				company_name = request.POST['company_name']
			except:
				company_name = None
			try:
				notes = request.POST['notes']
			except:
				notes = None
			cart = cartDetails(scart)
			if scart.user:
				user = scart.user
				device = None
			else:
				user = None
				device = scart.device
			couponlist = []
			for coupon in scart.coupon.all():
				temp = []
				temp.append(coupon.code)
				value = str(coupon.value)+'%' if coupon.discount_type == 'Percent' else coupon.value
				temp.append(value)
				couponlist.append(temp)
			ordr = Order(
				user = user,
				device = device,
				first_name=first_name,
				last_name=last_name,
				shopcart=scart,
				payment_id=payment_id,
				payment_mode=payment_mode,
				company_name=company_name,
				email=email,
				notes=notes,
				phone=phone,
				country=country,
				region=region,
				city=city,
				area=area,
				address=address,
				ship_name=cart.ship_name,
				ship_cost=cart.ship_cost,
				coupons = couponlist,
				coupon_disc=cart.coupon_discount,
				total=cart.subtotal + cart.ship_cost - cart.coupon_discount
			)
			ordr.user_currency = request.COOKIES['mycurrency']
			ordr.save()
			scart.on_order = True
			scart.save()
			try:
				return redirect('/')
			finally:
				# mail_config = EmailConfig.objects.get()
				# subject, from_email, to = 'Confirm order', mail_config.email_host_user, email
				# text_content = 'Confirm order'
				# html_content = render_to_string('order-confirm.html', context={
				# 	'order': ordr,
				# 	'currency': Currency.objects.get(code = request.COOKIES['mycurrency']),
				# 	'domain': get_current_site(request).domain
				# })
				# msg = EmailMultiAlternatives(subject, text_content, from_email, [to], connection=backend)
				# msg.attach_alternative(html_content, "text/html")
				# msg.send()
				pass
	else:
		# import requests
		# urls = "https://fcsapi.com/api-v2/forex/converter?symbol=BDT/USD&amount=1&access_key=ohHkx8n2tCX9BBoaGvFUwY"
		# resp = requests.get(urls)
		# print("1 ----------> ", resp.json())
		category = Category.objects.all()
		countrys = Country.objects.all()
		paypal = PaymentMethod.objects.filter(name='paypal').first()
		cashon = PaymentMethod.objects.filter(name='cashon').first()
		context = {
			'countrys': countrys,
			'paypal': paypal,
			'cashon': cashon,
		}
		return render(request, 'product/checkout.html', context)

def AddtoWishlist(request):
	device = request.COOKIES['device']
	product = Product.objects.get(id= request.POST['id'])
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
	cart_type = request.COOKIES['cart']
	if cart_type == 'ucart':
		scart = ShopCart.objects.get(user = request.user, on_order=False)
	else:
		scart = ShopCart.objects.get(device = device, on_order=False)
	cart_pro_list = []
	for cart in scart.carts.all():
		cart_pro_list.append(cart.product)
	if product in wlist.product.all():
		wlist.product.remove(product)
		return JsonResponse({'type': 'remove', 'msg': 'Product successfully removed from wishlist.'})
	elif product in cart_pro_list:
		return JsonResponse({'type': 'fail', 'msg': 'Product already exist to your cart.'})
	else:
		wlist.product.add(product)
		return JsonResponse({'type': 'add', 'msg': 'Product successfully added to wishlist.'})

def WishList(request):
	# wishlist = Wishlist.objects.filter(user = request.user)
	context = {
		'category_disable': True
	}
	return render(request, 'product/wishlist.html', context)

def WishItemDelete(request):
	get_wishlist = Wishlist.objects.get(id = request.POST["wishlist_id"])
	pro = Product.objects.get(id = request.POST['product_id'])
	get_wishlist.product.remove(pro)
	data = {
		'msg': "Success"
	}
	return JsonResponse(data)

def PlaceOrder(request):
	if request.method == "POST":
		if request.POST['diff-address'] == 'on':
			country = Country.objects.get(id = request.POST['add-country']).name
			region = Region.objects.get(id = request.POST['add-region']).name
			city = City.objects.get(id = request.POST['add-city']).name
			area = Area.objects.get(id = request.POST['add-area']).name
			address = request.POST['address']
		else:
			address_book = AddressBook.objects.get(id = request.POST['address_book'])
			country = address_book.country.name
			region = address_book.region.name
			city = address_book.city.name
			area = address_book.area.name
			address = address_book.address
			
		scart = ShopCart.objects.get(id = request.POST['shopcartid'])
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		email = request.POST['email']
		phone = request.POST['phone']
		payment_mode: request.POST['payment_mode']
		payment_id: request.POST['payment_id']
		try:
			company_name = request.POST['company_name']
		except:
			company_name = None
		try:
			notes = request.POST['notes']
		except:
			notes = None
		cart = cartDetails(scart)
		if scart.user:
			user = scart.user
			device = None
		else:
			user = None
			device = scart.device
		ordr = Order(
			user = user,
			device = device,
			first_name=first_name,
			last_name=last_name,
			shopcart=scart,
			payment_id=payment_id,
			payment_mode=payment_mode,
			company_name=company_name,
			email=email,
			notes=notes,
			phone=phone,
			country=country,
			region=region,
			city=city,
			area=area,
			address=address,
			ship_name=cart.ship_name,
			ship_cost=cart.ship_cost,
			coupon_disc=cart.coupon_discount,
			total=cart.subtotal + cart.ship_cost - cart.coupon_discount,
			paid=0
		)
		ordr.save()
		return HttpResponse(str(usr.first_name))

class Invoice(TemplateView):
	template_name = "account/invoice.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		ordr = Order.objects.get(id = kwargs['id'])
		context['order'] = Order.objects.get(id = kwargs['id'])
		cart = cartDetails(ordr.shopcart)
		context['due'] = ordr.total if ordr.payment_mode == 'cash' and ordr.status != 'completed' else 0
		context['category_disable'] = True
		return context

from django.http import HttpResponse
from django.views.generic import View

from .utils import render_to_pdf

class GeneratePdf(View):
	def get(self, request, *args, **kwargs):
		crncy = Currency.objects.get(code = request.COOKIES['mycurrency'])
		ordr = Order.objects.get(id = kwargs['id'])
		try:
			context = {
				'order': Order.objects.get(id = kwargs['id']),
				'rate': crncy.rate,
				'symbol': crncy.symbol_native,
				'due': ordr.total if ordr.payment_mode == 'cash' and ordr.status != 'completed' else 0
			}
			pdf = render_to_pdf('account/invoice_pdf.html', context)
		except:
			context = {
				'order': Order.objects.get(id = kwargs['id']),
				'rate': crncy.rate,
				'symbol': f'{crncy.code} ',
				'due': ordr.total if ordr.payment_mode == 'cash' and ordr.status != 'completed' else 0
			}
			pdf = render_to_pdf('account/invoice_pdf.html', context)

		if pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			filename = 'Invoice_%s.pdf' %(f"{kwargs['id']}")
			content = "inline; filename=%s" %(filename)
			download = request.GET.get("download")
			if download:
				content = "attachment; filename='%s'" %(filename)
			response['Content-Disposition'] = content
			return response
		return HttpResponse("Not found")

