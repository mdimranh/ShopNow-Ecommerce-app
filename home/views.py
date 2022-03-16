from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from setting.models import Slider, Banner, TeamInfo, Aboutus, ContactMessage, ProductCarousel, Menus
from product.models import Category, Subcategory, Group, Product, Brands, RecentlyView
from .forms import ContactMessageForm
from order.models import ShopCart
from .models import SearchKeyword

from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime, date

from django.contrib import messages

from django.core import serializers

def Home(request):
    # categorys = Category.objects.all()
    # subcategorys = Subcategory.objects.all()
    brand = Brands.objects.all()
    groups = Group.objects.all()
    # menus = Menus.objects.all().exclude(active=False).order_by('position')
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
    hot_product = Product.objects.filter(enable=True, hot_deal_end__gt = date.today())
    product_carousel = ProductCarousel.objects.filter(enable = True)
    recently_view = RecentlyView.objects.all().order_by("-on_create")
    context = {
        'brand': brand,
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
    teaminfo = TeamInfo.objects.all()
    aboutus = Aboutus.objects.all().first()
    context = {
        'teaminfo': teaminfo,
        'aboutus': aboutus
    }
    return render(request, 'shop/about.html', context)

def ContactUs(request):
    if request.method == 'POST':
        # form = ContactForm(request.POST)
        # if form.is_valid():
        #     data = ContactMessage()
        #     data.name = form.cleaned_data['name']
        #     data.email = form.cleaned_data['email']
        #     data.subject = form.cleaned_data['subject']
        #     data.message = form.cleaned_data['message']
        #     data.ip = request.META.get('REMOTE_ADDR')
        #     data.save()
        #     messages.success(request, 'Your message has been sent.')
        #     return redirect(request.path_info)
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        subject = request.POST['subject']
        message = request.POST['message']
        ip = request.META.get('REMOTE_ADDR')
        msg = ContactMessage(
            name = name,
            email = email,
            # phone = phone,
            subject=subject,
            ip = ip,
            message=message
        )
        msg.save()
        return redirect(request.path_info)
        
    teaminfo = TeamInfo.objects.all()
    aboutus = Aboutus.objects.all().first()
    context = {
        'aboutus': aboutus,
        'form': ContactMessageForm,
    }
    return render(request, 'shop/contact.html', context)

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
        teaminfo = TeamInfo.objects.all()
        aboutus = Aboutus.objects.all().first()
        if SearchKeyword.objects.filter(keyword=query).exists():
            searchKey = SearchKeyword.objects.get(keyword=query)
            searchKey.hit += 1
            searchKey.result = products.count()
            searchKey.save()
        else:
            searchKey = SearchKeyword(
                keyword = query,
                hit = 1,
                result = Product.objects.filter(title__icontains = query).count()
            )
            searchKey.save()
        return render(request, 'product/category.html', {'product': page_obj})