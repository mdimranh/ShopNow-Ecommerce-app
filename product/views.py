from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.views.generic import DetailView
from .models import Product, Images, Review
from product.models import Category, Group, Subcategory, RecentlyView
from django.core.paginator import Paginator
from django.db.models import Q, Sum

from setting.models import Menus

from django.template.defaultfilters import slugify

from django.http.response import JsonResponse

import datetime

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from django.db.models import Count

def ProductDetails(request, id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            username = request.user.first_name+' '+request.user.last_name
            user = request.user
        else:
            username = request.POST['user_name']
            user = ''
        pro_id = request.POST['id']
        rating = (int(request.POST['rating'])*100)/5
        comment = request.POST['comment']
        pro = Product.objects.get(id = pro_id)
        if request.user.is_authenticated:
            if Review.objects.filter(user = request.user, product = pro).exists():
                rvw = Review.objects.get(user = request.user, product=pro)
                rvw.rating = rating
                rvw.comment = comment
                rvw.save()
                pro.rate = (pro.rate + rating)/2
                pro.save()
                return redirect(request.path_info)
            else:
                rvw = Review(
                    product=pro,
                    user = user,
                    user_name=username,
                    rating = rating,
                    comment = comment
                )
                rvw.save()
                return redirect(request.path_info)
        else:
            rvw = Review(
                product=pro,
                user_name=username,
                rating = rating,
                comment = comment
            )
            rvw.save()
            return redirect(request.path_info)

    else:
        product = Product.objects.get(id = id)
        product.total_view += 1
        product.save()
        total_review = Review.objects.filter(product = product).count()
        if total_review > 0:
            total_rating = float(Review.objects.filter(product = product).aggregate(Sum('rating'))['rating__sum'])
            rating = total_rating/total_review
        else:
            rating = 0
        if RecentlyView.objects.filter(product__id=id).exists():
            recent_pro = RecentlyView.objects.get(product__id = id)
            recent_pro.on_create = datetime.datetime.now()
            recent_pro.save()
        else:
            recent_pro = RecentlyView.objects.create(product = product)
            recent_pro.save()
        menus = Menus.objects.all().exclude(active=False).order_by('position')
        images = Images.objects.filter(product=product)
        categorys = Category.objects.all()
        context = {
            'product': product,
            'images': images,
            'category': categorys,
            'total_review': total_review,
            'rating': rating,
            'menus': menus
        }
        return render(request, 'product/product-details.html', context)

class CategoryProduct(View):

    def get(self, request, id, slug):
        if Category.objects.filter(id = id, slug = slug).exists():
            product = Product.objects.filter(category__id = id).order_by('rate')
        elif Group.objects.filter(id = id, slug = slug).exists():
            product = Product.objects.filter(group__id = id).order_by('rate')
        elif Subcategory.objects.filter(id = id, slug = slug).exists():
            product = Product.objects.filter(subcategory__id = id).order_by('rate')

        paginator = Paginator(product, 12) # Show 12 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        categories = Category.objects.all()
        context = {
            'product': page_obj,
            'id': id,
            'slug': slug, 
            'categories': categories
        }
        return render(request, 'product/category.html', context)

    def post(self, request, id, slug):
        if request.POST['sortby'] == 'new_old':
            if Category.objects.filter(id = id, slug = slug).exists():
                product = Product.objects.filter(category__id = id).order_by('-created_at')
            elif Group.objects.filter(id = id, slug = slug).exists():
                product = Product.objects.filter(group__id = id).order_by('-created_at')
            elif Subcategory.objects.filter(id = id, slug = slug).exists():
                product = Product.objects.filter(subcategory__id = id).order_by('-created_at')
        elif request.POST['sortby'] == 'old_new':
            if Category.objects.filter(id = id, slug = slug).exists():
                product = Product.objects.filter(category__id = id).order_by('created_at')
            elif Group.objects.filter(id = id, slug = slug).exists():
                product = Product.objects.filter(group__id = id).order_by('created_at')
            elif Subcategory.objects.filter(id = id, slug = slug).exists():
                product = Product.objects.filter(subcategory__id = id).order_by('created_at')
        elif request.POST['sortby'] == 'rate':
            if Category.objects.filter(id = id, slug = slug).exists():
                product = Product.objects.filter(category__id = id).order_by('-rate')
            elif Group.objects.filter(id = id, slug = slug).exists():
                product = Product.objects.filter(group__id = id).order_by('-rate')
            elif Subcategory.objects.filter(id = id, slug = slug).exists():
                product = Product.objects.filter(subcategory__id = id).order_by('-rate')

        paginator = Paginator(product, 12) # Show 12 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        categories = Category.objects.all()
        context = {
            'product': page_obj,
            'id': id,
            'slug': slug, 
            'categories': categories,
            'sortby': request.POST['sortby']
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
            category = request.POST['category_id']
            group = []
            if category:
                groups = Category.objects.get(id = category).groups.all()
                for grp in groups:
                    gs = {
                        "id": str(grp.id),
                        "name": grp.name,
                    }
                    group.append(gs)
                # group = {p.name:p.id for p in groups}
            return JsonResponse(data = group, safe=False)
        else:
            group = request.data['group_id']
            subcategory = {}
            if group:
                subcategorys = Group.objects.get(id = group).subcategorys.all()
                subcategory = {p.name:p.id for p in subcategorys}
            return JsonResponse(data = subcategory, safe=False)

class ControlCategoryList(APIView):
    permission_classes = [IsAuthenticated,]
    def post(self, request, format = None):
        if 'category_id' in request.POST:
            category = request.data['category_id']
            group = []
            if category:
                groups = Category.objects.get(id = category).groups.all()
                for grp in groups:
                    gs = {
                        "id": str(grp.id),
                        "name": grp.name,
                    }
                    group.append(gs)
                # group = {p.name:p.id for p in groups}
            return JsonResponse(data = group, safe=False)
        else:
            group = request.data['group_id']
            subcat = []
            if group:
                subcats = Group.objects.get(id = group).subcategorys.all()
                for item in subcats:
                    subcat_item = {
                        "id": str(item.id),
                        "name": item.name,
                    }
                    subcat.append(subcat_item)
                # group = {p.name:p.id for p in groups}
            return JsonResponse(data = subcat, safe=False)
