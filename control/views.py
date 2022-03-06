from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from product.models import Product
from setting.models import Menus
from home.models import SearchKeyword
from django.contrib.auth.models import User

from django.contrib.auth.models import User, auth

from accounts.models import Profile
from setting.models import Slider, Banner, TeamInfo, Aboutus, ContactMessage, ProductCarousel, Menus
from product.models import Category, Subcategory, Group, Product, Brands, RecentlyView
from order.models import ShopCart

from datetime import datetime

def Dashboard(request):
	total_product = Product.objects.all().count()
	total_customer = User.objects.filter(is_staff=False, is_superuser=False).count()
	search = SearchKeyword.objects.all().order_by("-updated_at")
	context = {
		"total_product": total_product,
		"total_customer": total_customer,
		"search": search,
		"dashboard_sec": True
	}
	return render(request, "control/index.html", context)

def Menu(request):
	if request.method == 'POST':
		# print("id-------->", len(request.POST['id']))
		if len(request.POST['id']) == 0:
			enable = True if request.POST.get("menu-enable", False) == 'on' else False
			menu = Menus(
				name = request.POST['menu-name'],
				style = request.POST['menu-style'],
				icon = request.POST['menu-icon'],
				active = enable
			)
			menu.save()
			if request.POST.getlist('menu-category')[0].split(',')[0] != '':
				for i in request.POST.getlist('menu-category')[0].split(','):
					menu.categorys.add(Category.objects.get(id = i))
			if request.POST.getlist('menu-group')[0].split(',')[0] != '':
				for i in request.POST.getlist('menu-group')[0].split(','):
					menu.groups.add(Group.objects.get(id = i))
			if request.POST.getlist('menu-subcategory')[0].split(',')[0] != '':
				for i in request.POST.getlist('menu-subcategory')[0].split(','):
					menu.subcategorys.add(Subcategory.objects.get(id = i))
			menu.save()
		else:
			get_menu = Menus.objects.get(id = request.POST['id'])
			get_menu.active = True if request.POST.get("menu-enable") == 'on' else False
			get_menu.name = request.POST['menu-name']
			get_menu.style = request.POST['menu-style']
			get_menu.icon = request.POST['menu-icon']
			get_menu.save()
			get_menu.categorys.clear()
			get_menu.groups.clear()
			get_menu.subcategorys.clear()
			for i in request.POST.getlist('menu-category')[0].split(','):
				get_menu.categorys.add(Category.objects.get(id = i))
			if request.POST.getlist('menu-group')[0].split(',')[0] != '':
				for i in request.POST.getlist('menu-group')[0].split(','):
					get_menu.groups.add(Group.objects.get(id = i))
			if request.POST.getlist('menu-subcategory')[0].split(',')[0] != '':
				for i in request.POST.getlist('menu-subcategory')[0].split(','):
					get_menu.subcategorys.add(Subcategory.objects.get(id = i))
			get_menu.save()
		return redirect(request.path_info)

	allmenus = Menus.objects.all().order_by('position')
	categorys = Category.objects.all()
	groups = Group.objects.all()
	subcategories = Subcategory.objects.all()
	context = {
		"menus": allmenus,
		'categorys': categorys,
		'groups': groups,
		'subcategories': subcategories,
		'menu_sec': True
	}
	return render(request, "control/menu.html", context)

def MenuUpdate(request):
	menu_id = request.POST['menu_id'].split(',')
	if request.POST["action"] == 'update':
		p = 1
		for id in menu_id:
			get_menu = Menus.objects.get(id = id)
			get_menu.position = p
			get_menu.save()
			p+=1
		context = {
			"msg": "updated",
			"id": menu_id
		}
		return JsonResponse(context)
	else:
		get_menu = Menus.objects.get(id = request.POST['menu_id'])
		get_menu.delete()
		context = {
			"id": menu_id,
			"msg": "deleted",
		}
		return JsonResponse(context)

def Message(request):
	msg = ContactMessage.objects.all()
	context = {
		'messages': msg,
		'message_sec': True
	}
	return render(request, "control/message.html", context)

def MessageDetails(request, id):
	if request.method == "POST":
		msg = ContactMessage.objects.get(id = request.POST["id"])
		msg.note = request.POST["note"]
		msg.save()
		return redirect(request.path_info)
	msg = ContactMessage.objects.get(id = id)
	msg.status = "Read"
	msg.save()
	context = {
		'message': msg,
		'message_sec': True
	}
	return render(request, "control/message.html", context)

def Login(request):
	if request.method == "POST":
		email = request.POST['email']
		password = request.POST['password']
		user = auth.authenticate(username=email, password=password)

		if user is not None:
			if user.is_superuser:
				auth.login(request, user)
				pro = Profile.objects.get(user = user)
				pro.online = True
				pro.save()
				total_product = Product.objects.all().count()
				context = {
					"total_product": total_product
				}
				return render(request, "control/index.html", context)
			else:
				auth.login(request, user)
				pro = Profile.objects.get(user = user)
				pro.online = True
				pro.save()
				categorys = Category.objects.all()
				subcategorys = Subcategory.objects.all()
				brand = Brands.objects.all()
				groups = Group.objects.all()
				menus = Menus.objects.all()
				product = Product.objects.all()
				total_cost = 0
				item = 0
				shopcart = False
				if request.user.is_authenticated:
					shopcart = ShopCart.objects.filter(user = request.user)
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
					item = shopcart.count()
				new_product = Product.objects.filter(status=True).order_by('-id')
				new_product_cat = Product.objects.filter(status=True).distinct("category")
				hot_product = Product.objects.filter(status=True, hot_deal__gt = datetime.now())
				product_carousel = ProductCarousel.objects.filter(enable = True)
				recently_view = RecentlyView.objects.all().order_by("-on_create")
				context = {
					'category': categorys,
					'subcategory': subcategorys,
					'brand': brand,
					'group': groups,
					'menus': menus,
					'shopcart': shopcart,
					'product': product,
					'new_product': new_product,
					'new_product_cat': new_product_cat,
					'hot_product': hot_product,
					'procaro': product_carousel,
					'recent_view': recently_view,
					'cost': total_cost,
					'item': item
				}
				return render(request, 'home/home.html', context)
		else:
			messages.error(request, "Invalid username or password!")
			return render(request, "control/login.html")

	return render(request, "control/login.html")


def Users(request):
	users = User.objects.all()
	perm = ContentType.objects.all()
	context = {
		"users": users,
		"user_sec": True,
		"permis": perm
	}
	return render(request, "control/user.html", context)

from django.contrib.contenttypes.models import ContentType
def UserDetails(request, id):
	user = User.objects.get(id = id)
	perm = ContentType.objects.all()
	context = {
		"user_info": user,
		"user_sec": True,
		"permis": perm
	}
	return render(request, "control/user.html", context)
