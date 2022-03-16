from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .models import Profile, AddressBook
from setting.models import Slider, Banner, TeamInfo, Aboutus, ContactMessage
from product.models import Category, Product
from order.models import ShopCart
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.models import User, auth
from django.contrib import messages

from region.models import Country, Region, City, Area
from accounts.models import AddressBook

# def Account(request):
#     if request.method == "POST":
#         if 'first_name' in request.POST:
#             first_name = request.POST['first_name']
#             last_name = request.POST['last_name']
#             email = request.POST['email']
#             password = request.POST['password']

#             user = User.objects.create_user(username = email, first_name = first_name, last_name = last_name, email = email)
#             user.set_password(password)
#             user.save()
#             Profile.objects.create(user = user)
#             return JsonResponse({'msg': "Account create successfully. please login first", 'success': 'yes'})
#         else:
#             email = request.POST['email']
#             password = request.POST['password']
#             user = auth.authenticate(username=email, password=password)

#             if user is not None:
#                 auth.login(request, user)
#                 pro = Profile.objects.get(user = user)
#                 pro.online = True
#                 pro.save()
#                 cart = ShopCart.objects.filter(user = user).order_by('created_at')
#                 total_cost = 0
#                 cart_serialize = []
#                 cs={}
#                 for item in cart:
#                     price = item.product.main_price - (item.product.main_price * item.product.discount / 100)
#                     cost = price*item.quantity
#                     total_cost += cost
#                     cs = {
#                         "id": item.id,
#                         "category": item.product.category.name,
#                         "title": item.product.title,
#                         "image": item.product.image,
#                         "main_price": str(item.product.main_price),
#                         "price": str(item.product.main_price - (item.product.main_price * item.product.discount / 100)),
#                         "discount": str(item.product.discount),
#                         "amount": item.quantity
#                     }
#                     cart_serialize.append(cs)


#                 for item in cart[:1]:
#                     if item.coupon:
#                         if item.coupon.discount_type == 'fixed':
#                             total_cost -= item.coupon.value
#                         else:
#                             total_cost = total_cost - (total_cost * item.coupon.value / 100)
#                 item = cart.count()
#                 context = {
#                     'item':item,
#                     'cost':total_cost,
#                     'msg': 'Login Successfull',
#                     'cart': cart_serialize,
#                     'name': user.first_name+" "+user.last_name
#                 }
#                 return JsonResponse(context)
#             else:
#                 msg = 'Invalid username or password!'
#                 return JsonResponse({'msg': msg})
#         return HttpResponse({"msg": 'Something is wrong'})
#     return render(request, "account/login.html")


def Account(request):
    if request.method == "POST":
        if 'signup-first-name' in request.POST:
            first_name = request.POST['signup-first-name']
            last_name = request.POST['signup-last-name']
            email = request.POST['signup-email']
            password = request.POST['signup-password']

            user = User.objects.create_user(username = email, first_name = first_name, last_name = last_name, email = email)
            user.set_password(password)
            user.save()
            Profile.objects.create(user = user)
            return redirect(request.path_info)
        else:
            email = request.POST['signin-email']
            password = request.POST['signin-password']
            user = auth.authenticate(username=email, password=password)

            if user is not None:
                auth.login(request, user)
                pro = Profile.objects.get(user = user)
                pro.online = True
                pro.save()
                return redirect('profile')
            else:
                msg = 'Invalid username or password!'
                return JsonResponse({'msg': msg})
        return HttpResponse({"msg": 'Something is wrong'})
    return render(request, "account/login.html")

def ProfileView(request):
    if request.method == 'POST':
        if 'ab-name' in request.POST:
            if request.POST.get('default') == 'on':
                default = True
                for ab in AddressBook.objects.filter(default = 'True'):
                    ab.default = False
                    ab.save()
            else: default = False
            user = request.user
            name = request.POST['ab-name']
            phone = request.POST['ab-phone']
            if request.POST['ab-country'] != 'null':
                country = Country.objects.get(id = request.POST['ab-country'])
            else: country = None
            if request.POST['ab-region'] != 'null':
                region = Region.objects.get(id = request.POST['ab-region'])
            else: region = None
            if request.POST['ab-city'] != 'null':
                city = City.objects.get(id = request.POST['ab-city'])
            else: city = None
            if request.POST['ab-area'] != 'null':
                area = Area.objects.get(id = request.POST['ab-area'])
            else: area = None
            address = request.POST['ab-address']
            address_book = AddressBook(
                user=user, name=name, phone=phone, country=country, region=region, city=city, area=area, address=address, default=default
            )
            address_book.save()
            return redirect(request.path_info)
    total_cost = 0
    item = 0
    countrys = Country.objects.all()
    address_book = AddressBook.objects.filter(user = request.user)
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
        context = {
            'mycart': shopcart,
            'cost': total_cost,
            'item': item,
            'address_book': address_book,
            'countrys': countrys
        }
    else:
        context = {
            'category': categorys,
        }
    return render(request, 'account/profile.html', context)

def Logout(request):
    user = request.user
    pro = Profile.objects.get(user = user)
    pro.online = False
    pro.save()
    auth.logout(request)
    return redirect('/')

import json
# def GetCity(request):
#     id = request.POST['id']
#     city = []
#     f = open('bd-districts.json', 'r', encoding='utf-8')
#     data = json.load(f)
#     for i in data['districts']:
#         if i['division_id'] == id:
#             city.append((i['name'], i["id"]))
#     f.close()
#     return JsonResponse(data = city, safe=False)


def GetRegion(request):
    region_list = []
    for region in Country.objects.get(id = request.POST['id']).region.all():
        region_list.append((region.name, region.id))
    return JsonResponse(data = region_list, safe=False)

def GetCity(request):
    city_list = []
    for city in Region.objects.get(id = request.POST['id']).city.all():
        city_list.append((city.name, city.id))
    return JsonResponse(data = city_list, safe=False)

def GetArea(request):
    area_list = []
    for area in City.objects.get(id = request.POST['id']).area.all():
        area_list.append((area.name, area.id))
    return JsonResponse(data = area_list, safe=False)