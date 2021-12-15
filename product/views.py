from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import DetailView
from .models import Product, Images
from home.models import ShopInfo
from product.models import Category

from django.core.paginator import Paginator

def ProductDetails(request, id):
    product = Product.objects.get(id = id)
    images = Images.objects.filter(product=product)
    shopinfo = ShopInfo.objects.first()
    categorys = Category.objects.all()
    context = {
        'product': product,
        'images': images,
        'shopinfo': shopinfo,
        'category': categorys
    }
    return render(request, 'product/product-details.html', context)

def CategoryProduct(request, id, slug):
    categorys = Category.objects.all()
    shopinfo = ShopInfo.objects.first()
    category = Category.objects.get(id = id)
    if category.parent is not None:
        product = Product.objects.filter(category = category)
    else:
        product = Product.objects.filter(category__parent = category)

    pd = []
    for i in range(100):
        for p in product:
            pd.append(p)
    paginator = Paginator(pd, 12) # Show 12 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'product/category-product.html', {'product': page_obj, 'category': categorys, 'shopinfo': shopinfo, 'cat': category})