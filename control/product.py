from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from product.models import Product, Category, Group, Subcategory
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from product.models import Images, Options, Option, Brands

def Products(request):
    if 'name' and 'main-price' in request.POST:
        name = request.POST["name"]
        short_info = request.POST["short-desc"]
        amount = request.POST["quantity"]
        status = True if request.POST.get("enable", False) == 'on' else False
        category = Category.objects.get(id = request.POST["category"])
        if len(request.POST["group"]) > 0:
            group = Group.objects.filter(id = request.POST["group"]).first()
        else:
            group = None
        if len(request.POST["subcategory"]) > 0:
            subcategory = Subcategory.objects.filter(id = request.POST["subcategory"]).first()
        else:
            subcategory = None
        main_price = ((request.POST["main-price"]).replace("৳", "")).replace(",", "")
        if len(request.POST["discount"]) > 0:
            discount = request.POST["discount"]
        else:
            discount = 0
        discount_type = request.POST.get("discount-type", None)
        image = request.FILES['thumbnail']
        fs = FileSystemStorage("media/product/")
        filename = fs.save(image.name, image)
        image_url = settings.MEDIA_URL+"product/"+filename
        meta_title = request.POST["meta-title"]
        meta_keywords = request.POST["meta-keywords"]
        meta_descriptions = request.POST["meta-descriptions"]
        related_product = request.POST['related-products']
        size = request.POST["size"]
        color = request.POST.getlist("color")
        option_names = request.POST.getlist("option-name")
        option_style = request.POST.getlist("option-style")
        count = request.POST.getlist("option-count")
        labels = request.POST.getlist("options-option-name")
        prices = request.POST.getlist("option-price")
        hot_deal_start = request.POST["hot-deal-start"] if len(request.POST["hot-deal-start"]) > 0 else None
        hot_deal_end = request.POST["hot-deal-end"] if len(request.POST["hot-deal-end"]) > 0 else None
        hot_deal_discount = request.POST["hot-deal-discount"] if len(request.POST["hot-deal-discount"]) > 0 else None
        hot_deal_discount_type = request.POST["hot-deal-discount-type"]
        hot_deal_free_shipping = True if request.POST.get("hot-deal-free-shipping", False) == 'on' else False
        description = request.POST["description"]
        additional_info = request.POST["additional-info"]
        shipping_info = request.POST["shipping-info"]
        unique_key = request.POST["unique"]
        create_product = Product(
                title = name,
                short_info = short_info,
                amount = amount,
                enable = status,
                category = category,
                group = group,
                subcategory = subcategory,
                main_price = main_price,
                discount = discount,
                discount_type = discount_type,
                image = image_url,
                meta_title = meta_title,
                meta_keywords = meta_keywords,
                meta_descriptions = meta_descriptions,
                related_product = related_product,
                size = size,
                color = color,
                hot_deal_start = hot_deal_start,
                hot_deal_end = hot_deal_end,
                hot_deal_discount = hot_deal_discount,
                hot_deal_discount_type = hot_deal_discount_type,
                hot_deal_free_shipping = hot_deal_free_shipping,
                description = description,
                additional_info = additional_info,
                shipping_info = shipping_info,
                unique = unique_key
        )
        create_product.save()
        lab_pri = []
        for label in labels:
            lab_pri.append((label, prices[labels.index(label)]))
        print(lab_pri)

        c = 0
        for op_name in option_names:
            opt = Options(
                name = op_name,
                style = option_style[c]
            )
            opt.save()
            for i in range(int(count[c])):
                op = Option(
                    label = lab_pri[0][0],
                    price = lab_pri[0][1]
                )
                op.save()
                opt.option.add(op)
                opt.save()
                lab_pri.remove(lab_pri[0])
            c+=1
            create_product.option.add(opt)
            create_product.save()
        return redirect(request.path_info)
    products = Product.objects.all()
    categorys = Category.objects.all()
    context = {
        "products": products,
        "categorys": categorys,
        "product_sec": True,
        "all_product_sec": True,
    }
    return render(request, "control/product.html", context)

def ImagesSave(request):
    if request.method == "POST":
        imgs = [request.FILES.get('images[%d]' % i)
        for i in range(0, len(request.FILES))]
        print(len(imgs))
        idlist = []
        urllist = []
        for img in imgs:
            fs = FileSystemStorage("media/product/additional/")
            filename = fs.save(img.name, img)
            image_url = settings.MEDIA_URL+"product/additional/"+filename
            new_image = Images(
                image = image_url,
                unique = request.POST["unique"]
            )
            new_image.save()
            idlist.append(new_image.id)
            urllist.append(new_image.image)
        context = {
            'ids' : idlist,
            'urls': urllist
        }
        return JsonResponse(context)
    return HttpResponse("Fail")

def deleteImage(request):
    if request.method == 'POST':
        Images.objects.get(id = request.POST['id']).delete()
        return JsonResponse({'id': request.POST['id']})
class EditProduct(View):
    def get(self, request, id):
        product = Product.objects.get(id = id)
        products = Product.objects.all()
        categorys = Category.objects.all()
        additional_image = Images.objects.filter(unique=product.unique)
        for img in additional_image:
            img.product = product
            img.save()
        context = {
            "product_details": product,
            "categorys": categorys,
            'images': additional_image,
            'products': products,
            "product_sec": True,
            "edit_product_sec": True
        }
        return render(request, "control/product.html", context)

    def post(self, request, id):
        pro = Product.objects.get(id = id)
        for removed_img_id in request.POST['remove-images']:
            Images.objects.get(id = removed_img_id).delete()

        name = request.POST["name"]
        short_info = request.POST["short-desc"]
        amount = request.POST["quantity"]
        status = True if request.POST.get("enable", False) == 'on' else False
        category = Category.objects.get(id = request.POST["category"])
        if len(request.POST["group"]) > 0:
            group = Group.objects.filter(id = request.POST["group"]).first()
        else:
            group = None
        if len(request.POST["subcategory"]) > 0:
            subcategory = Subcategory.objects.filter(id = request.POST["subcategory"]).first()
        else:
            subcategory = None
        main_price = ((request.POST["main-price"]).replace("৳", "")).replace(",", "")
        if len(request.POST["discount"]) > 0:
            discount = request.POST["discount"]
        else:
            discount = 0
        discount_type = request.POST.get("discount-type", None)
        meta_title = request.POST["meta-title"]
        meta_keywords = request.POST["meta-keywords"]
        meta_descriptions = request.POST["meta-descriptions"]
        related_product = request.POST['related-products']
        size = request.POST["size"]
        color = request.POST.getlist("color")
        option_names = request.POST.getlist("option-name")
        option_style = request.POST.getlist("option-style")
        count = request.POST.getlist("option-count")
        labels = request.POST.getlist("options-option-name")
        prices = request.POST.getlist("option-price")
        hot_deal_start = request.POST["hot-deal-start"] if len(request.POST["hot-deal-start"]) > 0 else None
        hot_deal_end = request.POST["hot-deal-end"] if len(request.POST["hot-deal-end"]) > 0 else None
        hot_deal_discount = request.POST["hot-deal-discount"] if len(request.POST["hot-deal-discount"]) > 0 else None
        hot_deal_discount_type = request.POST["hot-deal-discount-type"]
        hot_deal_free_shipping = True if request.POST.get("hot-deal-free-shipping", False) == 'on' else False
        description = request.POST["description"]
        additional_info = request.POST["additional-info"]
        shipping_info = request.POST["shipping-info"]
        
        pro.title = name
        pro.short_info = short_info
        pro.amount = amount
        pro.enable = status
        pro.category = category
        pro.group = group
        pro.subcategory = subcategory
        pro.main_price = main_price
        pro.discount = discount
        pro.discount_type = discount_type
        pro.meta_title = meta_title
        pro.meta_keywords = meta_keywords
        pro.meta_descriptions = meta_descriptions
        pro.related_product = related_product
        pro.size = size
        pro.color = color
        pro.hot_deal_start = hot_deal_start
        pro.hot_deal_end = hot_deal_end
        pro.hot_deal_discount = hot_deal_discount
        pro.hot_deal_discount_type = hot_deal_discount_type
        pro.hot_deal_free_shipping = hot_deal_free_shipping
        pro.description = description
        pro.additional_info = additional_info
        pro.shipping_info = shipping_info
        for option in pro.option.all():
            option.delete()
        pro.save()

        try:
            image = request.FILES['thumbnail']
            fs = FileSystemStorage("media/product/")
            filename = fs.save(image.name, image)
            image_url = settings.MEDIA_URL+"product/"+filename
            pro.image = image_url
            pro.save()
        except:
            pass

        lab_pri = []
        for label in labels:
            lab_pri.append((label, prices[labels.index(label)]))
        print(lab_pri)

        c = 0
        for op_name in option_names:
            opt = Options(
                name = op_name,
                style = option_style[c]
            )
            opt.save()
            for i in range(int(count[c])):
                op = Option(
                    label = lab_pri[0][0],
                    price = lab_pri[0][1]
                )
                op.save()
                opt.option.add(op)
                opt.save()
                lab_pri.remove(lab_pri[0])
            c+=1
            pro.option.add(opt)
        return redirect(request.path_info)

def deleteProduct(request):
    total_pro = len(request.POST["product"].split(','))
    for pro_id in request.POST["product"].split(','):
        pro = Product.objects.get(id = pro_id)
        for op in pro.option.all():
            for opt in op.option.all():
                opt.delete()
            op.delete()
        pro.delete()
    context = {
        'total' : total_pro
    }
    return JsonResponse(context)

def CategoryView(request):
    if request.method == 'POST':
        if request.POST['type'] == 'new-cat':
            cat = Category(
                name = request.POST['category-name'],
                icon = request.POST['icon'],
                searchable = True if request.POST.get('search', False) == 'on' else False,
                enable = True if request.POST.get('enable', False) == 'on' else False
            )
            cat.save()
        if request.POST['type'] == 'category':
            if 'category-name' in request.POST:
                cat = Category.objects.get(id = request.POST['id'])
                cat.name = request.POST['category-name']
                cat.icon = request.POST['icon']
                cat.searchable = True if request.POST.get('search', False) == 'on' else False
                cat.enable = True if request.POST.get('enable', False) == 'on' else False
                cat.save()
            elif 'group-name' in request.POST:
                grp = Group(
                    name = request.POST['group-name'],
                    category = Category.objects.get(id = request.POST['id']),
                    searchable = True if request.POST.get('search', False) == 'on' else False,
                    enable = True if request.POST.get('enable', False) == 'on' else False
                )
                grp.save()
        elif request.POST['type'] == 'group':
            if 'group-name' in request.POST:
                grp = Group.objects.get(id = request.POST['id'])
                grp.name = request.POST['group-name']
                grp.searchable = True if request.POST.get('search', False) == 'on' else False
                grp.enable = True if request.POST.get('enable', False) == 'on' else False
                grp.save()
            elif 'subcategory-name' in request.POST:
                subcat = Subcategory(
                    name = request.POST['subcategory-name'],
                    group = Group.objects.get(id = request.POST['id']),
                    category = Category.objects.get(id = Group.objects.get(id = request.POST['id']).category.id),
                    searchable = True if request.POST.get('search', False) == 'on' else False,
                    enable = True if request.POST.get('enable', False) == 'on' else False
                )
                subcat.save()
        elif request.POST['type'] == 'subcategory':
            subcat = Subcategory.objects.get(id = request.POST['id'])
            subcat.name = request.POST['subcategory-name']
            subcat.searchable = True if request.POST.get('search', False) == 'on' else False
            subcat.enable = True if request.POST.get('enable', False) == 'on' else False
            subcat.save()    
        return redirect(request.path_info)

    categorys = Category.objects.all()
    context = {
        "categorys": categorys,
        "product_sec": True,
        "category_sec": True
    }
    return render(request, "control/category.html", context)

def CategoryDelete(request, id):
    cat = Category.objects.filter(id = id).first()
    cat.delete()
    return redirect("/control/category")

class BrandView(View):
    def get(self, request):
        all_brand = Brands.objects.all()
        context = {
            'brands': all_brand,
            "product_sec": True,
            'brand_sec': True
        }
        return render(request, 'control/brand.html', context)
    def post(self, request):
        brnd = Brands(
            name = request.POST['name'],
            logo = request.FILES['logo']
        )
        brnd.save()
        return redirect(request.path_info)

class BrandDetails(View):
    def get(self, request, id):
        brand = Brands.objects.get(id = id)
        context = {
            'brand': brand,
            "product_sec": True,
            'brand_sec': True
        }
        return render(request, 'control/brand.html', context)
    def post(self, request, id):
        brand = Brands.objects.get(id = id)
        brand.name = request.POST['name']
        try:
            brand.logo = request.FILES['logo']
        except:
            pass
        brand.save()
        return redirect(request.path_info)

def deleteBrand(request):
    total_brand = len(request.POST["brands"].split(','))
    for brand_id in request.POST["brands"].split(','):
        Brands.objects.get(id = brand_id).delete()
    context = {
        'total' : total_brand
    }
    return JsonResponse(context)

def GroupDelete(request, id):
    grp = Group.objects.filter(id = id).first()
    grp.delete()
    return redirect("/control/category")

def SubcategoryDelete(request, id):
    subcat = Subcategory.objects.filter(id = id).first()
    subcat.delete()
    return redirect("/control/category")

def Coupon(request):
    context = {
        "coupon_sec": True
    }
    return render(request, "control/coupon.html", context)