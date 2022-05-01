from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic import View, DetailView
from django.contrib import messages

from django.contrib.auth.models import User, auth, Permission
from django.contrib.auth.models import Group as UserGroup

from home.models import SearchKeyword
from accounts.models import Profile
from setting.models import Slider, Banner, TeamInfo, Aboutus, ContactMessage, ProductCarousel, Menus
from product.models import Category, Subcategory, Group, Product, Brands, RecentlyView
from order.models import ShopCart, Order

from django.db.models import Sum, Count
from django.db.models.functions import TruncDay, TruncDate
from django.contrib.contenttypes.models import ContentType

from django.utils.timezone import now
from datetime import datetime, timedelta

def Dashboard(request):
	total_product = Product.objects.all().count()
	total_customer = User.objects.filter(is_staff=False, is_superuser=False).count()
	total_order = Order.objects.all().count()
	total_sales = Order.objects.all().aggregate(Sum("total"))['total__sum']
	search = SearchKeyword.objects.all().order_by("-updated_at")
	orders = Order.objects.all().order_by("order_date")

	def getList(day, status):
		day = now().date() - timedelta(days = day)
		if status == 'all':
			query = Order.objects.filter(order_date__gte = day)
			datas = query.annotate(
				day = TruncDay("order_date"),
				date = TruncDate('order_date'),
				order_count = Count("order_date__date")
			).values(
				'day',
				'date',
				'order_count'
			)
		else:
			query = Order.objects.filter(update__gte = day, status = status)
			datas = query.annotate(
					day = TruncDay("update"),
					date = TruncDate('update'),
					order_count = Count("update__date")
				).values(
					'day',
					'date',
					'order_count'
				)

		lst = []
		for d in range(7):
			lst.append((day, day.strftime('%A'), 0))
			day += timedelta(days = 1)
		for i in datas:
			x = 0
			for a, b, c in lst:
				if a == i['date']:
					lst[x] = (a, b, i['order_count'])
				x += 1
		return lst

	order_data = getList(6, 'all')
	complete_data = getList(6, 'completed')
	pending_data = getList(6, 'pending')
	cancel_data = getList(6, 'canceled')
	ppayment_data = getList(6, 'pending_payment')

	context = {
		"total_product": total_product,
		"total_customer": total_customer,
		"total_sales": total_sales,
		'total_order': total_order,
		'order_data': order_data,
		'complete_data': complete_data,
		'pending_data': pending_data,
		'cancel_data': cancel_data,
		'ppayment_data': ppayment_data,
		"search": search,
		'orders': orders,
		"dashboard_sec": True
	}
	return render(request, "control/index.html", context)

def Menu(request):
	if request.method == 'POST':
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
				pro = Profile.objects.get_or_create()
				return redirect('/control')
			else:
				auth.login(request, user)
				pro = Profile.objects.get_or_create()
				return redirect('/')
		else:
			messages.error(request, "Invalid username or password!")
			return render(request, "control/login.html")

	return render(request, "control/login.html")


class Users(View):
		
	def get(self, request):
		users = User.objects.all()
		grp = UserGroup.objects.all()
		context = {
			"users": users,
			"user_sec": True,
			'user_list_sec':True,
			'group': grp
		}
		return render(request, "control/user.html", context)

	def post(self, request):
		staff = True if request.POST.get('staff') == 'on' else False
		admin = True if request.POST.get('admin') == 'on' else False
		active = True if request.POST.get('active') == 'on' else False
		usr = User(
			first_name = request.POST['first_name'],
			last_name = request.POST['last_name'],
			email = request.POST['email'],
			password = request.POST['password'],
			username = request.POST['email'],
			is_superuser = admin,
			is_staff = staff,
			is_active = active
		)
		usr.save()
		if staff == True:
			role = UserGroup.objects.get(id = request.POST['role'])
			usr.groups.add(role)
			usr.save()
		return redirect(request.path_info)
		

class UserDetails(View):
		
	def get(self, request, id):
		user = User.objects.get(id = id)
		grp = UserGroup.objects.all()
		context = {
			"user_info": user,
			"user_sec": True,
			'edit_user_sec':True,
			'group': grp
		}
		return render(request, "control/user.html", context)

	def post(self, request, id):
		usr = User.objects.get(id = request.POST['id'])
		staff = True if request.POST.get('staff') == 'on' else False
		admin = True if request.POST.get('admin') == 'on' else False
		active = True if request.POST.get('active') == 'on' else False
		usr.first_name = request.POST['first_name']
		usr.last_name = request.POST['last_name']
		usr.email = request.POST['email']
		usr.username = request.POST['email']
		usr.is_superuser = admin
		usr.is_staff = staff
		usr.is_active = active
		if len(request.POST['password']) > 1:
			usr.set_password(request.POST['password'])
		if staff == True:
			role = UserGroup.objects.get(id = request.POST['role'])
			usr.groups.clear()
			usr.groups.add(role)
		else:
			usr.groups.clear()
		usr.save()
		return redirect(request.path_info)

class Roles(View):
			
	def get(self, request):
		roles = UserGroup.objects.all()
		perm = ContentType.objects.all().order_by("app_label")
		grp = UserGroup.objects.all()
		context = {
			"roles": roles,
			"user_sec": True,
			'role_list_sec':True,
			"permis": perm
		}
		return render(request, "control/role.html", context)

	def post(self, request):
		role = UserGroup(
			name=request.POST['name']
		)
		role.save()
		prm = list(Permission.objects.all().values_list('id', flat=True))
		for ids in prm:
			try:
				if request.POST[str(ids)] == 'allow':
					role.permissions.add(ids)
					role.save()
			except:
				pass
		return redirect(request.path_info)

class RoleDetails(View):
		
	def get(self, request, id):
		role_details = UserGroup.objects.get(id=id)
		perm_list = list(role_details.permissions.all().values_list('id', flat=True))
		perm = ContentType.objects.all().order_by("app_label")
		context = {
			"role_details": role_details,
			"user_sec": True,
			'role_list_sec':True,
			"permis": perm,
			'perm_list': perm_list
		}
		return render(request, "control/role.html", context)

	def post(self, request, id):
		role = UserGroup.objects.get(id = id)
		role.name = request.POST['name']
		role.permissions.clear()
		prm = list(Permission.objects.all().values_list('id', flat=True))
		for ids in prm:
			try:
				if request.POST[str(ids)] == 'allow':
					role.permissions.add(ids)
					role.save()
			except:
				pass
		return redirect(request.path_info)
