from django.shortcuts import render
from django.http import HttpResponse
from product.models import Product
from setting.models import Menus

from django.contrib.auth.models import User, auth

from setting.models import Slider, Banner, TeamInfo, Aboutus, ContactMessage, ProductCarousel, Menus
from product.models import Category, Subcategory, Group, Product, Brands, RecentlyView
from order.models import ShopCart

from datetime import datetime

def Dashboard(request):
    total_product = Product.objects.all().count()
    context = {
        "total_product": total_product
    }
    return render(request, "control/index.html", context)

def Menu(request):
    allmenus = Menus.objects.all()
    context = {
        "menus": allmenus
    }
    return render(request, "control/menu.html", context)

def Login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username=email, password=password)

        if user is not None:
            if user.is_superuser:
                print("Yes ---------")
                auth.login(request, user)
                total_product = Product.objects.all().count()
                context = {
                    "total_product": total_product
                }
                return render(request, "control/index.html", context)
            else:
                auth.login(request, user)
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
    return render(request, "control/login.html")
