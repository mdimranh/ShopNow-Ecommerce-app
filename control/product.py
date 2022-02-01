from django.shortcuts import render
from product.models import Product, Category

def Products(request):
    products = Product.objects.all()
    categorys = Category.objects.all()
    context = {
        "products": products,
        "categorys": categorys
    }
    return render(request, "control/product.html", context)

def EditProduct(request, id):
    product = Product.objects.get(id = id)
    categorys = Category.objects.all()
    context = {
        "product": product,
        "categorys": categorys
    }
    return render(request, "control/edit-product.html", context)

def CategoryView(request):
    categorys = Category.objects.all()
    context = {
        "categorys": categorys
    }
    return render(request, "control/category.html", context)

def Coupon(request):
    return render(request, "control/coupon.html")