from django.shortcuts import render
from product.models import Product, Category
from django.core.files.storage import FileSystemStorage
from django.conf import settings

def Products(request):
    if request.method == "POST":
        print("Multiple file --------------->> ",request.FILES.get("add-additional-image"))
        # name = request.POST["name"]
        # short_info = request.POST["short-desc"]
        # amount = request.POST["quantity"]
        # enable = request.POST.get("enable", None)
        # if enable == 'on':
        #     status = True
        # else:
        #     status = False
        # category = Category.objects.get(id = request.POST["category"])
        # main_price = ((request.POST["main-price"]).replace("৳", "")).replace(",", "")
        # image = request.FILES['thumbnail']
        # fs = FileSystemStorage("media/logo/")
        # filename = fs.save(image.name, image)
        # image_url = settings.MEDIA_URL+"product/"+filename
        # size = request.POST["size"]
        # meta_title = request.POST["meta-title"]
        # meta_keywords = request.POST["meta-keywords"]
        # meta_descriptions = request.POST["meta-descriptions"]
        # description = request.POST["description"]
        # additional_info = request.POST["additional-info"]
        # shipping_info = request.POST["shipping-info"]
        # discount = 0
        # create_product = Product(title = name, description = description, short_info = short_info, amount = amount, enable = status, category=category, main_price=main_price, image = image_url, size=size, meta_title=meta_title, meta_descriptions=meta_descriptions, meta_keywords=meta_keywords, additional_info=additional_info, shipping_info=shipping_info, discount=discount)
        # create_product.save()
    products = Product.objects.all()
    categorys = Category.objects.all()
    context = {
        "products": products,
        "categorys": categorys,
        "product_sec": True,
        "all_product_sec": True,
    }
    return render(request, "control/product.html", context)

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

def CategoryView(request):
    categorys = Category.objects.all()
    context = {
        "categorys": categorys,
        "product_sec": True,
        "category_sec": True
    }
    return render(request, "control/category.html", context)

def Coupon(request):
    context = {
        "coupon_sec": True
    }
    return render(request, "control/coupon.html", context)