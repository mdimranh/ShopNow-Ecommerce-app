from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .models import ShopCart
from product.models import Product

from home.models import ShopInfo
from product.models import Category

from django.core import serializers

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def AddtoCart(request):
    product_id = request.POST['id']
    product = Product.objects.get(id = product_id)
    if 'quantity' in request.POST:
        if product.amount < request.POST['quantity']:
            msg = f"We have only {product.amount} products"
            return HttpResponse(msg)
        else:
            quantity = request.POST['quantity']
    else:
        quantity = 1
    if ShopCart.objects.filter(product=product, user = request.user).exists():
        shopcart = ShopCart.objects.get(product=product, user = request.user)
        shopcart.quantity = int(shopcart.quantity) + 1
        shopcart.save()
        cart = ShopCart.objects.filter(user = request.user)
        total_cost = 0
        for item in cart:
            price = item.product.main_price - (item.product.main_price * item.product.discount / 100)
            cost = price*item.quantity
            total_cost += cost
        item = cart.count()
        return JsonResponse({'item':item, 'cost':total_cost})
    shopcart = ShopCart(
        product= product,
        user = request.user,
        quantity = quantity
    )
    shopcart.save()
    cart = ShopCart.objects.filter(user = request.user)
    total_cost = 0
    for item in cart:
        price = item.product.main_price - (item.product.main_price * item.product.discount / 100)
        cost = price*item.quantity
        total_cost += cost
    item = cart.count()
    return JsonResponse({'item':item, 'cost':total_cost})

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
    context = {
        'shopinfo': shopinfo,
        'category': categorys,
        'shopcart': shopcart
    }
    return render(request, 'order/shopping-cart.html', context)