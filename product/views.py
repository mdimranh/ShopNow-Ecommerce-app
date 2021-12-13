from django.shortcuts import render
from django.views.generic import DetailView
from .models import Product, Images
from home.models import ShopInfo
from product.models import Category

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
