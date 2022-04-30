from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse

from django.views.generic import View

from django.contrib import messages
from django.core import serializers

from setting.models import Slider, Banner, TeamInfo, Aboutus, ContactMessage, ProductCarousel, Menus
from product.models import Category, Subcategory, Group, Product, Brands, RecentlyView
from .forms import ContactMessageForm
from setting.models import Pages
from order.models import ShopCart, Order, Cart
from .models import SearchKeyword

from django.core.paginator import Paginator
from django.db.models import Q

from datetime import datetime, date, timedelta

def Home(request):
    brand = Brands.objects.all()
    groups = Group.objects.all()
    product = Product.objects.all()
    new_product = Product.objects.filter(enable=True).order_by('-id')
    new_product_cat = Product.objects.filter(enable=True).distinct("category")
    hot_product = Product.objects.filter(enable=True, hot_deal_end__gt = date.today())
    
    # List of best selling product
    bestSell_range = date.today() - timedelta(days = 30)
    best_sell = Order.objects.filter(order_date__gte = bestSell_range)
    bs_pro_list = []
    for order in best_sell:
        for cart in order.shopcart.carts.all():
            bs_pro_list.append(cart.product.id)
    bs_pro_list = sorted(bs_pro_list, key=lambda x:[bs_pro_list.count(x), x])
    bs_pro_list.reverse()
    bs_pro_list = list(dict.fromkeys(bs_pro_list))
    bs_pro = []
    for pro_id in bs_pro_list[:5]:
        bs_pro.append(Product.objects.get(id = pro_id))

    product_carousel = ProductCarousel.objects.filter(enable = True)
    recently_view = RecentlyView.objects.all().order_by("-on_create")
    ls = []
    latest_sold = Order.objects.all().order_by('order_date')
    for order in latest_sold:
        for cart in order.shopcart.carts.all():
            if cart.product not in ls:
                ls.append(cart.product)
                if len(ls) > 2:
                    break
        if len(ls) > 2:
            break
    print(ls)
    context = {
        'brand': brand,
        'product': product,
        'best_sold': bs_pro,
        'new_product': new_product,
        'new_product_cat': new_product_cat,
        'hot_product': hot_product,
        'latest_sold': ls,
        'procaro': product_carousel,
        'recent_view': recently_view,
    }
    return render(request, 'home/home.html', context)

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

def error_404(request, exception):
    return render(request, 'home/404.html')

class PageView(View):
    def get(self, request, slug, *args, **kwargs):
        page = Pages.objects.get(slug = slug)
        return render(request, 'home/page.html', context={
            'page': page
        })