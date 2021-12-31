from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import DetailView
from .models import Product, Images
from product.models import Category, Group, Subcategory
from django.core.paginator import Paginator

from django.template.defaultfilters import slugify

from django.http.response import JsonResponse

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

def ProductDetails(request, id):
    product = Product.objects.get(id = id)
    images = Images.objects.filter(product=product)
    categorys = Category.objects.all()
    context = {
        'product': product,
        'images': images,
        'category': categorys
    }
    return render(request, 'product/product-details.html', context)

def CategoryProduct(request, id, slug):
    if Category.objects.filter(id = id, slug = slug).exists():
        product = Product.objects.filter(category__id = id)
    elif Group.objects.filter(id = id, slug = slug).exists():
        product = Product.objects.filter(group__id = id)
    elif Subcategory.objects.filter(id = id, slug = slug).exists():
        product = Product.objects.filter(subcategory__id = id)

    pd = []
    for i in range(100):
        for p in product:
            pd.append(p)
    paginator = Paginator(pd, 12) # Show 12 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categorys = Category.objects.all()
    context = {
        'product': page_obj,
        'category': categorys
    }
    return render(request, 'product/category.html', context)

class CategoryGroupList(APIView):
    permission_classes = [IsAuthenticated,]
    def post(self, request, format = None):
        category = request.data['category_id']
        group = {}
        if category:
            groups = Category.objects.get(id = category).groups.all()
            group = {p.name:p.id for p in groups}
        return JsonResponse(data = group, safe=False)

class ProductGroupList(APIView):
    permission_classes = [IsAuthenticated,]
    def post(self, request, format = None):
        if 'category_id' in request.POST:
            category = request.data['category_id']
            group = {}
            if category:
                groups = Category.objects.get(id = category).groups.all()
                group = {p.name:p.id for p in groups}
            return JsonResponse(data = group, safe=False)
        else:
            group = request.data['group_id']
            subcategory = {}
            if group:
                subcategorys = Group.objects.get(id = group).subcategorys.all()
                subcategory = {p.name:p.id for p in subcategorys}
            return JsonResponse(data = subcategory, safe=False)