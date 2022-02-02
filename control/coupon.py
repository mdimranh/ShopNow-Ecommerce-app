from django.shortcuts import render
from product.models import Product, Category
from order.models import Coupon

def CouponView(request):
    products = Product.objects.all()
    categorys = Category.objects.all()
    coupons = Coupon.objects.all()
    context = {
        "products": products,
        "categories": categorys,
        "coupons": coupons
    }
    return render(request, "control/coupon.html", context)

def CouponDetails(request, id):
    cpn = Coupon.objects.get(id = id)
    products = Product.objects.all()
    categorys = Category.objects.all()
    context = {
        "products": products,
        "categorys": categorys,
        "coupon": cpn
    }
    return render(request, "control/edit-coupon.html", context)