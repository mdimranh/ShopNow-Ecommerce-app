from django.shortcuts import render
from django.http import HttpResponse
from product.models import Product

def Dashboard(request):
    total_product = Product.objects.all().count()
    context = {
        "total_product": total_product
    }
    return render(request, "admin/index.html", context)
