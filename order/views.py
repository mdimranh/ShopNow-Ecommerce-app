from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse, JsonResponse

from .models import ShopCart, Coupon
from product.models import Product

from setting.models import ShopInfo
from product.models import Category

import json

from django.core import serializers

from django.views.decorators.csrf import csrf_exempt
def AddtoCart(request):
    if 'update-quantity' in request.POST:
        cart = ShopCart.objects.get(id = request.POST['id'])
        if cart.product.amount < int(request.POST["update-quantity"]):
            msg = f"We have only {cart.product.amount} product"
        else:
            cart.quantity = request.POST['update-quantity']
            cart.save()
            msg = 'Successfull'
        return JsonResponse({'msg': msg})
    product_id = request.POST['id']
    if Product.objects.filter(id = product_id).exists():
        product = Product.objects.get(id = product_id)
        product_serialize = {
            "category": product.category.name,
            "title": product.title,
            "image": product.image.url,
            "main_price": str(product.main_price),
            "price": str(product.main_price - (product.main_price * product.discount / 100)),
            "discount": str(product.discount)
        }
        pro = json.dumps(product_serialize)
    if 'coupon_code' in request.POST:
        if Coupon.objects.filter(code = request.POST['coupon_code']).exists():
            coupon = Coupon.objects.get(code = request.POST['coupon_code'])
            cart = ShopCart.objects.filter(user = request.user)
            for item in cart:
                item.coupon = coupon
                item.save()
            total_cost = 0
            for item in cart:
                price = item.product.main_price - (item.product.main_price * item.product.discount / 100)
                cost = price*item.quantity
                total_cost += cost
            for item in cart[:1]:
                if item.coupon:
                    if item.coupon.discount_type == 'fixed':
                        total_cost -= item.coupon.value
                    else:
                        total_cost = total_cost - (total_cost * item.coupon.value / 100)
            item = cart.count()
            msg = "Coupon added successfully."
            if coupon.discount_type == 'fixed':
                value = "&#2547;"+str(coupon.value)
            else:
                value = str(coupon.value)+"%"
            return JsonResponse({'item':item, 'cost':total_cost, 'msg': msg, 'value': value})
        else:
            msg = "Not a valid code!"
            return JsonResponse({'added': 'fail', 'msg': msg})
    if ShopCart.objects.filter(product=product, user = request.user).exists():
        shopcart = ShopCart.objects.get(product=product, user = request.user)
        shopcart.quantity = int(shopcart.quantity) + 1
        shopcart.save()
        cart = ShopCart.objects.filter(user = request.user)
        total_cost = 0
        cart_serialize = []
        cs={}
        for item in cart:
            price = item.product.main_price - (item.product.main_price * item.product.discount / 100)
            cost = price*item.quantity
            total_cost += cost
            cs = {
                "category": item.product.category.name,
                "title": item.product.title,
                "image": item.product.image.url,
                "main_price": str(item.product.main_price),
                "price": str(item.product.main_price - (item.product.main_price * item.product.discount / 100)),
                "discount": str(item.product.discount),
                "amount": item.quantity
            }
            cart_serialize.append(cs)
        
        for item in cart[:1]:
            if item.coupon:
                if item.coupon.discount_type == 'fixed':
                    total_cost -= item.coupon.value
                else:
                    total_cost = total_cost - (total_cost * item.coupon.value / 100)
        item = cart.count()
        msg = "Product successfully added to cart!"
        return JsonResponse({'item':item, 'cost':total_cost, 'msg': msg, 'product': pro, 'cart': cart_serialize})
    shopcart = ShopCart(
        product= product,
        user = request.user,
        quantity = quantity
    )
    shopcart.save()
    cart = ShopCart.objects.filter(user = request.user)
    total_cost = 0
    cart_serialize = []
    cs={}
    for item in cart:
        price = item.product.main_price - (item.product.main_price * item.product.discount / 100)
        cost = price*item.quantity
        total_cost += cost
        cs = {
            "category": item.product.category.name,
            "title": item.product.title,
            "image": item.product.image.url,
            "main_price": str(item.product.main_price),
            "price": str(item.product.main_price - (item.product.main_price * item.product.discount / 100)),
            "discount": str(item.product.discount),
            "amount": item.quantity
        }
        cart_serialize.append(cs)


    for item in cart[:1]:
        if item.coupon:
            if item.coupon.discount_type == 'fixed':
                total_cost -= item.coupon.value
            else:
                total_cost = total_cost - (total_cost * item.coupon.value / 100)
    item = cart.count()
    msg = "Product successfully added to cart!"
    context = {
        'item':item,
        'cost':total_cost,
        'msg': msg,
        'product': pro,
        'cart': cart_serialize
    }
    return JsonResponse(context)

# import json
# @csrf_exempt
# def GetCart(request):
#     if request.method == 'POST':    
#         card = ShopCart.objects.filter(user = request.user)
#         card_list = []
#         for p in card:
#             if p.product.main_price > 0:
#                 price =  float(p.product.main_price - (p.product.main_price * p.product.discount / 100))
#             else:
#                 price = 0
#             card_list.append({"id": p.product.id, "name": p.product.title, "image": p.product.image.url, "price": price})
#         shop_cart = json.dumps(card_list)
#         return JsonResponse(shop_cart, safe=False)

def CartView(request):
    shopinfo = ShopInfo.objects.all().first()
    categorys = Category.objects.all()
    shopcart = ShopCart.objects.filter(user = request.user)
    total_cost = 0
    for item in shopcart:
        price = item.product.main_price - (item.product.main_price * item.product.discount / 100)
        cost = price*item.quantity
        total_cost += cost
    for item in shopcart[:1]:
        if item.coupon:
            if item.coupon.discount_type == 'Fixed':
                total_cost -= item.coupon.value
            else:
                total_cost = total_cost - (total_cost * item.coupon.value / 100)
    context = {
        'shopinfo': shopinfo,
        'category': categorys,
        'shopcart': shopcart,
        'cost': total_cost,
        'item': shopcart.count()
    }
    return render(request, 'product/cart.html', context)

def CartDelete(request, id):
    url = request.META.get('HTTP_REFERER')
    shopcart = ShopCart.objects.filter(user = request.user, product__id = id)
    shopcart.delete()
    return HttpResponseRedirect(url)

def Checkout(request):
    shopinfo = ShopInfo.objects.all().first()
    categorys = Category.objects.all()
    shopcart = ShopCart.objects.filter(user = request.user)
    total_cost = 0
    for item in shopcart:
        price = item.product.main_price - (item.product.main_price * item.product.discount / 100)
        cost = price*item.quantity
        total_cost += cost
    for item in shopcart[:1]:
        if item.coupon:
            if item.coupon.discount_type == 'Fixed':
                total_cost -= item.coupon.value
            else:
                total_cost = total_cost - (total_cost * item.coupon.value / 100)
    context = {
        'shopinfo': shopinfo,
        'category': categorys,
        'shopcart': shopcart,
        'cost': total_cost,
        'item': shopcart.count()
    }
    return render(request, 'order/checkout.html', context)