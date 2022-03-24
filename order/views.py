from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse, JsonResponse

from django.contrib.auth.models import User

from .models import ShopCart, Coupon, Wishlist
from product.models import Product

from product.models import Category
from region.models import Country, Region, City, Area

from order.models import ShippingMethod, PaymentMethod, Order
from accounts.models import AddressBook

import json

from django.core import serializers

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def AddtoCart(request):
    if 'update-quantity' in request.POST:
        cart = ShopCart.objects.get(id = request.POST['id'])
        if cart.product.amount < int(request.POST["update-quantity"]):
            msg = f"We have only {cart.product.amount} product"
            msg_type = 'fail'
            return JsonResponse({'msg':msg, 'msg_type':msg_type})
        else:
            cart.quantity = request.POST['update-quantity']
            cart.save()
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
                    "image": item.product.image,
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
            return JsonResponse({'item':item, 'cost':total_cost, 'msg': msg, 'cart': cart_serialize})

    product_id = request.POST['id']
    if Product.objects.filter(id = product_id).exists():
        product = Product.objects.get(id = product_id)
        product_serialize = {
            "id": product.id,
            "category": product.category.name,
            "title": product.title,
            "image": product.image,
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
    if ShopCart.objects.filter(product=product, user = request.user, on_order=False).exists():
        shopcart = ShopCart.objects.get(product=product, user = request.user, on_order=False)
        shopcart.quantity = int(shopcart.quantity) + 1
        shopcart.save()
        if Wishlist.objects.filter(product__id = request.POST['id'], user = request.user).exists():
            Wishlist.objects.get(product__id = request.POST['id'], user = request.user).delete()
        cart = ShopCart.objects.filter(user = request.user, on_order=False)
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
                "image": item.product.image,
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
        quantity = request.POST['quantity']
    )
    shopcart.save()
    if Wishlist.objects.filter(product__id = request.POST['id'], user = request.user).exists():
        Wishlist.objects.get(product__id = request.POST['id'], user = request.user).delete()
    cart = ShopCart.objects.filter(user = request.user, on_order=False).order_by('created_at')
    total_cost = 0
    cart_serialize = []
    cs={}
    for item in cart:
        price = item.product.main_price - (item.product.main_price * item.product.discount / 100)
        cost = price*item.quantity
        total_cost += cost
        cs = {
            "id": item.id,
            "category": item.product.category.name,
            "title": item.product.title,
            "image": item.product.image,
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
        'category': categorys,
        'shopcart': shopcart,
        'cost': total_cost,
        'item': shopcart.count()
    }
    return render(request, 'product/cart.html', context)

def CartDelete(request):
    shopcart = ShopCart.objects.get(id = request.POST['id'])
    shopcart.delete()
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
            "image": item.product.image,
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
    msg = "Product successfully deleted"
    return JsonResponse({'item':item, 'cost':total_cost, 'msg': msg, 'cart': cart_serialize})

def Checkout(request):
    category = Category.objects.all()
    shopcart = ShopCart.objects.filter(user = request.user, on_order = False)
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
    countrys = Country.objects.all()
    local_shipping = ShippingMethod.objects.filter(method_type = 'local').first()
    free_shipping = ShippingMethod.objects.filter(method_type = 'free').first()
    paypal = PaymentMethod.objects.filter(name='paypal').first()
    context = {
        'category': category,
        'shopcart': shopcart,
        'cost': total_cost,
        'countrys': countrys,
        'local_shipping': local_shipping,
        'free_shipping': free_shipping,
        'paypal': paypal,
        'item': shopcart.count()
    }
    return render(request, 'product/checkout.html', context)

def AddtoWishlist(request):
    if Wishlist.objects.filter(product__id = request.POST['id'], user = request.user).exists():
        context = {
            'msg': 'Product already exist in wish list.'
        }
        return JsonResponse(context)
    wishlist = Wishlist(
        user = request.user,
        product = Product.objects.get(id = request.POST['id'])
    )
    wishlist.save()
    return JsonResponse({'msg': 'Successfully added.'})

def WishList(request):
    wishlist = Wishlist.objects.filter(user = request.user)
    context = {
        'wishlist' : wishlist
    }
    return render(request, 'product/wishlist.html', context)

def WishItemDelete(request):
    get_wishlist = Wishlist.objects.get(id = request.POST["id"])
    get_wishlist.delete()
    data = {
        'msg': "Success"
    }
    return JsonResponse(data)

def PlaceOrder(request):
    if request.method == "POST":
        usr = User.objects.get(id = request.POST['user_id'])
        if request.POST['diff_address'] == 'on':
            country = Country.objects.get(id = request.POST['ab_country']),
            region = Region.objects.get(id = request.POST['ab_region']),
            city = City.objects.get(id = request.POST['ab_city']),
            area = Area.objects.get(id = request.POST['ab_area']),
            address = request.POST['ab_address'],
        else:
            address_book = AddressBook.objects.get(id = request.POST['address_book'])
            country = address_book.country.name
            region = address_book.region.name
            city = address_book.city.name
            area = address_book.area.name
            address = address_book.address

        payment_id = request.POST['payment_id']
        company_name = request.POST['company_name']
        payment_mode = request.POST['payment_mode']
        email = request.POST['email']
        notes = request.POST['notes']
        phone = request.POST['phone']
        rate = request.POST['rate']
        total = request.POST['total']
        total_bdt = request.POST['total_bdt']
        shipping_fee = 0 if float(total_bdt) >= ShippingMethod.objects.get(method_type = 'free').fee else ShippingMethod.objects.get(method_type = 'local').fee
        ordr = Order(
            user = usr,
            payment_id = payment_id,
            payment_mode = payment_mode,
            company_name = company_name,
            email = email,
            phone = phone,
            notes = notes,
            country = country,
            region = region,
            city = city,
            area = area,
            address = address,
            rate = rate,
            shipping_fee = shipping_fee,
            shipping_method = ShippingMethod.objects.get(method_type = 'free') if shipping_fee == 0 else ShippingMethod.objects.get(method_type = 'local'),
            total = total,
            total_bdt = total_bdt,
        )
        ordr.save()
        get_shopcart = ShopCart.objects.filter(user = usr).exclude(on_order=True)
        for cart in get_shopcart:
            cart.order_id = ordr.id
            cart.on_order = True
            cart.save()
            ids = cart.product.id
            get_pro = Product.objects.get(id = ids)
            qntity = get_pro.amount - int(cart.quantity)
            if qntity < 0:
                qntity = 0
            get_pro.amount = qntity
            get_pro.save()
            ordr.shopcarts.add(cart)
            ordr.save()
        return HttpResponse(str(usr.first_name))