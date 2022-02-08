from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from setting.models import Slider, Banner, TeamInfo, Aboutus, ContactMessage, ProductCarousel, Menus
from product.models import Category, Subcategory, Group, Product, Brands, RecentlyView
from .forms import ContactMessageForm
from order.models import ShopCart

from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime

from django.contrib import messages

from django.core import serializers

def Home(request):
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
    new_product = Product.objects.filter(enable=True).order_by('-id')
    new_product_cat = Product.objects.filter(enable=True).distinct("category")
    hot_product = Product.objects.filter(enable=True, hot_deal__gt = datetime.now())
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

def AboutUs(request):
    category = Category.objects.all()
    teaminfo = TeamInfo.objects.all()
    aboutus = Aboutus.objects.all().first()
    context = {
        'category': category,
        'teaminfo': teaminfo,
        'aboutus': aboutus
    }
    return render(request, 'aboutus/about-us.html', context)

def ContactUs(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, 'Your message has been sent.')
            return redirect(request.path_info)
    categorys = Category.objects.all()
    teaminfo = TeamInfo.objects.all()
    aboutus = Aboutus.objects.all().first()
    context = {
        'category': categorys,
        'aboutus': aboutus,
        'form': ContactMessageForm
    }
    return render(request, 'aboutus/contact.html', context)

def SearchView(request):
    if request.method == 'POST':
        cat_id = request.POST['category']
        query = request.POST['query']
        if cat_id == '0':
            products = Product.objects.filter(title__icontains = query)
        else:
            products = Product.objects.filter(Q(category__id = cat_id, title__icontains = query) | Q(group__id = cat_id, title__icontains = query) | Q(subcategory__id = cat_id, title__icontains = query))
        paginator = Paginator(products, 12) # Show 12 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        categorys = Category.objects.all()
        teaminfo = TeamInfo.objects.all()
        aboutus = Aboutus.objects.all().first()
        return render(request, 'product/category.html', {'product': page_obj, 'category': categorys})