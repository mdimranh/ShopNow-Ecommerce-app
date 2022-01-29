from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from setting.models import Slider, Banner, TeamInfo, Aboutus, ContactMessage
from product.models import Category, Product
from order.models import ShopCart
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.models import User, auth
from django.contrib import messages

from region.models import State

def Account(request):
    if request.method == "POST":
        if 'first_name' in request.POST:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password = request.POST['password']

            user = User.objects.create_user(username = email, first_name = first_name, last_name = last_name, email = email)
            user.set_password(password)
            user.save()
            return JsonResponse({'msg': "Account create successfully. please login first", 'success': 'yes'})
        else:
            email = request.POST['email']
            password = request.POST['password']
            user = auth.authenticate(username=email, password=password)

            if user is not None:
                auth.login(request, user)
                cart = ShopCart.objects.filter(user = user).order_by('created_at')
                total_cost = 0
                cart_serialize = []
                cs={}
                for item in cart:
                    price = item.product.main_price - (item.product.main_price * item.product.discount / 100)
                    cost = price*item.quantity
                    total_cost += cost
                    cs = {
                        "id": item.id,
                        "category": item.product.category.name,
                        "title": item.product.title,
                        "image": item.product.image.url,
                        "main_price": str(item.product.main_price),
                        "price": str(item.product.main_price - (item.product.main_price * item.product.discount / 100)),
                        "discount": str(item.product.discount),
                        "amount": item.quantity
                    }
                    cart_serialize.append(cs)


                for item in cart[:1]:
                    if item.coupon:
                        if item.coupon.discount_type == 'fixed':
                            total_cost -= item.coupon.value
                        else:
                            total_cost = total_cost - (total_cost * item.coupon.value / 100)
                item = cart.count()
                context = {
                    'item':item,
                    'cost':total_cost,
                    'msg': 'Login Successfull',
                    'cart': cart_serialize,
                    'name': user.first_name+" "+user.last_name
                }
                return JsonResponse(context)
            else:
                msg = 'Invalid username or password!'
                return JsonResponse({'msg': msg})
    return HttpResponse({"msg": 'Something is wrong'})

def Profile(request):
    categorys = Category.objects.all()
    total_cost = 0
    item = 0
    state = State.objects.all()
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
            'category': categorys,
            'cost': total_cost,
            'item': item,
            'state': state
        }
    else:
        context = {
            'category': categorys,
        }
    return render(request, 'account/profile.html', context)

def Logout(request):
    auth.logout(request)
    return redirect('/')

import json
def GetCity(request):
    id = request.POST['id']
    city = []
    f = open('bd-districts.json', 'r', encoding='utf-8')
    data = json.load(f)
    for i in data['districts']:
        if i['division_id'] == id:
            city.append((i['name'], i["id"]))
    f.close()
    return JsonResponse(data = city, safe=False)

def GetArea(request):
    id = request.POST['id']
    area = []
    f = open('bd-upazilas.json', 'r', encoding='utf-8')
    data = json.load(f)
    for i in data['upazilas']:
        if i['district_id'] == id:
            area.append((i['name'], i["id"]))
    f.close()
    return JsonResponse(data = area, safe=False)