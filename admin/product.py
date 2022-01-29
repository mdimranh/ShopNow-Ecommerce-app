from django.shortcuts import render
from product.models import Product, Category

def Products(request):
    products = Product.objects.all()
    context = {
        "products": products
    }
    return render(request, "admin/product.html", context)

def EditProduct(request, id):
    product = Product.objects.get(id = id)
    categorys = Category.objects.all()
    context = {
        "product": product,
        "categorys": categorys
    }
    return render(request, "admin/edit-product.html", context)