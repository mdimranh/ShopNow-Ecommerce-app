from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from setting.models import Slider, Banner, TeamInfo, Aboutus, ContactMessage, ProductCarousel, Menus
from product.models import Category, Subcategory, Group, Product, Brands, RecentlyView
from .forms import ContactMessageForm
from order.models import ShopCart, Order
from .models import SearchKeyword

from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime, date, timedelta

from django.contrib import messages

from django.core import serializers

def Home(request):
    brand = Brands.objects.all()
    groups = Group.objects.all()
    product = Product.objects.all()
    new_product = Product.objects.filter(enable=True).order_by('-id')
    new_product_cat = Product.objects.filter(enable=True).distinct("category")
    hot_product = Product.objects.filter(enable=True, hot_deal_end__gt = date.today())
    bestSell_range = date.today() - timedelta(days = 6)
    best_sell = Order.objects.filter(order_date__gte = bestSell_range)
    bs_pro_list = []
    for scart in best_sell:
        bs_pro_list.append(scart.product.id)
    print("list---------->", bs_pro_list)
    product_carousel = ProductCarousel.objects.filter(enable = True)
    recently_view = RecentlyView.objects.all().order_by("-on_create")
    context = {
        'brand': brand,
        'product': product,
        'new_product': new_product,
        'new_product_cat': new_product_cat,
        'hot_product': hot_product,
        'procaro': product_carousel,
        'recent_view': recently_view,
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

        if 'sortby' in request.POST:
            if request.POST['sortby'] == 'rate':
                if cat_id == '0':
                    products = Product.objects.filter(title__icontains = query).order_by('rate')
                else:
                    products = Product.objects.filter(Q(category__id = cat_id, title__icontains = query) | Q(group__id = cat_id, title__icontains = query) | Q(subcategory__id = cat_id, title__icontains = query)).order_by('rate')
            if request.POST['sortby'] == 'new_old':
                if cat_id == '0':
                    products = Product.objects.filter(title__icontains = query).order_by('created_at')
                else:
                    products = Product.objects.filter(Q(category__id = cat_id, title__icontains = query) | Q(group__id = cat_id, title__icontains = query) | Q(subcategory__id = cat_id, title__icontains = query)).order_by('rate').order_by('created_at')
            if request.POST['sortby'] == 'old_new':
                if cat_id == '0':
                    products = Product.objects.filter(title__icontains = query).order_by('-created_at')
                else:
                    products = Product.objects.filter(Q(category__id = cat_id, title__icontains = query) | Q(group__id = cat_id, title__icontains = query) | Q(subcategory__id = cat_id, title__icontains = query)).order_by('-created_at')
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
            categories = Category.objects.all()
            context = {
                'product': page_obj,
                'query': query,
                'categories': categories,
                'sortby': request.POST['sortby'],
                'cat_id': cat_id
            }
            return render(request, 'product/category.html', context)

        else:
            cat_id = request.POST['category']
            query = request.POST['query']
            if cat_id == '0':
                products = Product.objects.filter(title__icontains = query).order_by('rate')
            else:
                products = Product.objects.filter(Q(category__id = cat_id, title__icontains = query) | Q(group__id = cat_id, title__icontains = query) | Q(subcategory__id = cat_id, title__icontains = query)).order_by('rate')
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
            categories = Category.objects.all()
            context = {
                'product': page_obj,
                'query': query,
                'categories': categories,
                'cat_id': cat_id
            }
            return render(request, 'product/category.html', context)