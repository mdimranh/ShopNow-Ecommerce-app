from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from setting.models import ShopInfo, Sliding, Banner, TeamInfo, Aboutus, ContactMessage
from product.models import Category, Product
from order.models import ShopCart
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.models import User, auth
from django.contrib import messages

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
                total_cost = 0
                item = 0
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
                    'cost': total_cost,
                    'item': item
                }
                return HttpResponse(context)
            else:
                msg = 'Invalid username or password!'
                return HttpResponse({'msg': msg})
    return HttpResponse({"msg": 'Something is wrong'})

def Logout(request):
    auth.logout(request)
    return redirect('/')