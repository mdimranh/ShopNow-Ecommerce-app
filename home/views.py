from django.shortcuts import render
from .models import ShopInfo, Sliding, Banner
from product.models import Category, Product

def Home(request):
    shopinfo = ShopInfo.objects.all().first()
    categorys = Category.objects.all()
    slider = Sliding.objects.filter(active = True)
    banner = Banner.objects.filter(active=True, big_banner = False)
    big_banner = Banner.objects.filter(active=True, big_banner = True)
    category = Category.objects.all()
    product = Product.objects.all()
    new_product = Product.objects.filter(status=True).order_by('created_at')
    context = {
        'shopinfo': shopinfo,
        'category': categorys,
        'slider': slider,
        'banner': banner,
        'big_banner': big_banner,
        'category': category,
        'product': product,
        'new_product': new_product
    }
    return render(request, 'home/index-2.html', context)

def AboutUs(request):
    return render(request, 'others/about-us.html')
