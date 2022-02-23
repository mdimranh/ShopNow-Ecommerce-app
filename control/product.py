from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from product.models import Product, Category, Group, Subcategory
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from product.models import Images

# @csrf_exempt
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

        lab_pri = []
        for label in labels:
            lab_pri.append((label, prices[labels.index(label)]))

        options = []
        temp = []
        op = []
        c = 0
        for op_name in option_names:
            temp.append(op_name)
            temp.append(option_style[c])
            for i in range(int(count[c])):
                op.append(lab_pri[0])
                lab_pri.remove(lab_pri[0])
            temp.append(op)
            options.append(temp)
            op = []
            temp = []
            c+=1
        option = options
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
                option = option,
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
        images = request.FILES['images']
        fs = FileSystemStorage("media/product/additional/")
        filename = fs.save(images.name, images)
        image_url = settings.MEDIA_URL+"product/additional/"+filename
        new_image = Images(
            image = image_url,
            unique = request.POST["unique"]
        )
        new_image.save()
        return HttpResponse("Success")
    return HttpResponse("Fail")

def EditProduct(request, id):
    product = Product.objects.get(id = id)
    categorys = Category.objects.all()
    context = {
        "product_details": product,
        "categorys": categorys,
        "product_sec": True,
        "edit_product_sec": True
    }
    return render(request, "control/product.html", context)

def deleteProduct(request):
    total_pro = len(request.POST["product"].split(','))
    for pro_id in request.POST["product"].split(','):
        Product.objects.get(id = pro_id).delete()
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