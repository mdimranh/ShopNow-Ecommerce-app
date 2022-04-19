from django.shortcuts import render, HttpResponseRedirect, redirect
from django.http import HttpResponse, JsonResponse

from django.contrib.auth.models import User

from .models import ShopCart, Coupon, Wishlist
from setting.models import Currency
from product.models import Product

from product.models import Category
from region.models import Country, Region, City, Area

from order.models import ShippingMethod, PaymentMethod, Order, Cart
from accounts.models import AddressBook

import json

from django.core import serializers
from django.views import View

from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
# @csrf_exempt
# def AddtoCart(request):
    # if 'update-quantity' in request.POST:
    #     getcart = ShopCart.objects.get(id = request.POST['id'])
    #     cart = getcart.products.all()
    #     if cart.product.amount < int(request.POST["update-quantity"]):
    #         msg = f"We have only {cart.product.amount} product"
    #         msg_type = 'fail'
    #         return JsonResponse({'msg':msg, 'msg_type':msg_type})
    #     else:
    #         cart.quantity = request.POST['update-quantity']
    #         cart.save()
    #         price = cart.cost
    #         cart = ShopCart.objects.filter(user = request.user)
    #         total_cost = 0
    #         cart_serialize = []
    #         cs={}
    #         for item in cart:
    #             price = item.product.main_price - (item.product.main_price * item.product.discount / 100)
    #             cost = price*item.quantity
    #             total_cost += cost
    #             subtotal = total_cost
    #             cs = {
    #                 "category": item.product.category.name,
    #                 "title": item.product.title,
    #                 "image": item.product.image,
    #                 "main_price": str(item.product.main_price),
    #                 "price": str(item.product.main_price - (item.product.main_price * item.product.discount / 100)),
    #                 "discount": str(item.product.discount),
    #                 "amount": item.quantity
    #             }
    #             cart_serialize.append(cs)
            
    #         for item in cart[:1]:
    #             if item.coupon:
    #                 if item.coupon.discount_type == 'fixed':
    #                     total_cost -= item.coupon.value
    #                 else:
    #                     total_cost = total_cost - (total_cost * item.coupon.value / 100)
    #         local_shipping = ShippingMethod.objects.filter(method_type = 'local').first()
    #         free_shipping = ShippingMethod.objects.filter(method_type = 'free').first()
    #         if total_cost <= float(free_shipping.fee):
    #             total_cost += local_shipping.fee
    #         item = cart.count()
    #         msg = "Product successfully added to cart!"
    #         return JsonResponse({'item':item, 'cost':total_cost, 'update_price': price,  'subtotal': subtotal, 'msg': msg, 'cart': cart_serialize})

    # product_id = request.POST['id']
    # if Product.objects.filter(id = product_id).exists():
    #     product = Product.objects.get(id = product_id)
    #     product_serialize = {
    #         "id": product.id,
    #         "category": product.category.name,
    #         "title": product.title,
    #         "image": product.image,
    #         "main_price": str(product.main_price),
    #         "price": str(product.main_price - (product.main_price * product.discount / 100)),
    #         "discount": str(product.discount)
    #     }
    #     pro = json.dumps(product_serialize)
    # if 'coupon_code' in request.POST:
    #     if Coupon.objects.filter(code = request.POST['coupon_code']).exists():
    #         coupon = Coupon.objects.get(code = request.POST['coupon_code'])
    #         cart = ShopCart.objects.filter(user = request.user)
    #         for item in cart:
    #             item.coupon = coupon
    #             item.save()
    #         total_cost = 0
    #         for item in cart:
    #             price = item.product.main_price - (item.product.main_price * item.product.discount / 100)
    #             cost = price*item.quantity
    #             total_cost += cost
    #         for item in cart[:1]:
    #             if item.coupon:
    #                 if item.coupon.discount_type == 'fixed':
    #                     total_cost -= item.coupon.value
    #                 else:
    #                     total_cost = total_cost - (total_cost * item.coupon.value / 100)
    #         item = cart.count()
    #         msg = "Coupon added successfully."
    #         if coupon.discount_type == 'fixed':
    #             value = "&#2547;"+str(coupon.value)
    #         else:
    #             value = str(coupon.value)+"%"
    #         return JsonResponse({'item':item, 'cost':total_cost, 'msg': msg, 'value': value})
    #     else:
    #         msg = "Not a valid code!"
    #         return JsonResponse({'added': 'fail', 'msg': msg})
    # if ShopCart.objects.filter(product=product, user = request.user, on_order=False).exists():
    #     shopcart = ShopCart.objects.get(product=product, user = request.user, on_order=False)
    #     shopcart.quantity = int(shopcart.quantity) + 1
    #     shopcart.save()
    #     if Wishlist.objects.filter(product__id = request.POST['id'], user = request.user).exists():
    #         Wishlist.objects.get(product__id = request.POST['id'], user = request.user).delete()
    #     cart = ShopCart.objects.filter(user = request.user, on_order=False)
    #     total_cost = 0
    #     cart_serialize = []
    #     cs={}
    #     for item in cart:
    #         price = item.product.main_price - (item.product.main_price * item.product.discount / 100)
    #         cost = price*item.quantity
    #         total_cost += cost
    #         cs = {
    #             "category": item.product.category.name,
    #             "title": item.product.title,
    #             "image": item.product.image,
    #             "main_price": str(item.product.main_price),
    #             "price": str(item.product.main_price - (item.product.main_price * item.product.discount / 100)),
    #             "discount": str(item.product.discount),
    #             "amount": item.quantity
    #         }
    #         cart_serialize.append(cs)
        
    #     for item in cart[:1]:
    #         if item.coupon:
    #             if item.coupon.discount_type == 'fixed':
    #                 total_cost -= item.coupon.value
    #             else:
    #                 total_cost = total_cost - (total_cost * item.coupon.value / 100)
    #     item = cart.count()
    #     msg = "Product successfully added to cart!"
    #     return JsonResponse({'item':item, 'cost':total_cost, 'msg': msg, 'product': pro, 'cart': cart_serialize})
    # print('options---------->', request.POST.getlist('options[]'))
    # cart = Cart(
    #     product= product,
    #     quantity = request.POST['quantity'],
    #     options = request.POST.getlist('options[]')
    # )
    # cart.save()
    # if Wishlist.objects.filter(product__id = request.POST['id'], user = request.user).exists():
    #     Wishlist.objects.get(product__id = request.POST['id'], user = request.user).delete()
    # cart = ShopCart.objects.filter(user = request.user, on_order=False).order_by('created_at')
    # total_cost = 0
    # cart_serialize = []
    # cs={}
    # for item in cart:
    #     price = item.product.main_price - (item.product.main_price * item.product.discount / 100)
    #     cost = price*item.quantity
    #     total_cost += cost
    #     cs = {
    #         "id": item.id,
    #         "category": item.product.category.name,
    #         "title": item.product.title,
    #         "image": item.product.image,
    #         "main_price": str(item.product.main_price),
    #         "price": str(item.product.main_price - (item.product.main_price * item.product.discount / 100)),
    #         "discount": str(item.product.discount),
    #         "amount": item.quantity
    #     }
    #     cart_serialize.append(cs)


    # for item in cart[:1]:
    #     if item.coupon:
    #         if item.coupon.discount_type == 'fixed':
    #             total_cost -= item.coupon.value
    #         else:
    #             total_cost = total_cost - (total_cost * item.coupon.value / 100)
    # item = cart.count()
    # msg = "Product successfully added to cart!"
    # context = {
    #     'item':item,
    #     'cost':total_cost,
    #     'msg': msg,
    #     'product': pro,
    #     'cart': cart_serialize
    # }
    # return JsonResponse(context)

class AddToCart(View):
    def post(self, request):
        if 'update-quantity' in request.POST:
            getcart = Cart.objects.get(id = request.POST['id'])
            if getcart.product.amount < int(request.POST["update-quantity"]):
                msg = f"We have only {getcart.product.amount} product"
                msg_type = 'fail'
                return JsonResponse({'msg':msg, 'msg_type':msg_type})
            else:
                getcart.quantity = request.POST['update-quantity']
                getcart.save()
                scart = ShopCart.objects.get(user = request.user, on_order=False)
                total_cost = 0
                cart_serialize = []
                cs={}
                subtotal = 0
                for cart in scart.carts.all():
                    price = cart.product.main_price - (cart.product.main_price * cart.product.discount / 100)
                    cost = price*cart.quantity
                    total_cost += cost
                    subtotal = total_cost
                    cs = {
                        "id": cart.id,
                        "category": cart.product.category.name,
                        "title": cart.product.title,
                        "image": cart.product.image,
                        "main_price": str(cart.product.main_price),
                        "price": str(cart.product.main_price - (cart.product.main_price * cart.product.discount / 100)),
                        "discount": str(cart.product.discount),
                        "amount": cart.quantity
                    }
                    cart_serialize.append(cs)
                
                if scart.coupon.all().count() > 0:
                    cpn_dis = 0
                    for cpn in scart.coupon.all():
                        cpn_dis += cpn.value if cpn.discount_type.lower() == 'fixed' else total_cost * cpn.value / 100
                    total_cost -= cpn_dis
                
                local_shipping = ShippingMethod.objects.filter(method_type = 'local').first()
                free_shipping = ShippingMethod.objects.filter(method_type = 'free').first()
                if total_cost <= float(free_shipping.fee):
                    total_cost += local_shipping.fee
                item = scart.carts.all().count()
                msg = "Product successfully added to cart!"
                return JsonResponse({'item':item, 'cost':total_cost, 'update_price': price,  'subtotal': subtotal, 'msg': msg, 'cart': cart_serialize})
        else:
            cart_type = request.COOKIES['cart']
            if cart_type == 'ucart':
                scart = ShopCart.objects.get(user = request.user, on_order = False)
            else:
                scart = ShopCart.objects.get(device = request.COOKIES['device'], on_order = False)
            pro_id = int(request.POST['id'])
            if Product.objects.filter(id = pro_id).exists():
                pro_list = list(scart.carts.values_list('product__id', flat=True))
                if pro_id in pro_list:
                    return JsonResponse({'msg': "Product already exist"})
                pro = Product.objects.get(id = pro_id)
                if pro.amount < 0:
                    return JsonResponse({'msg': "Out of stock"})
                else:
                    cart = Cart(
                        product= pro,
                        quantity = request.POST['quantity'],
                        options = request.POST.getlist('options[]')
                    )
                    cart.save()
                    scart.carts.add(cart)
                    scart.save()
                    try:
                        Wishlist.objects.filter(product = pro, user = request.user).first().delete()
                    except:
                        pass
                    total_cost = 0
                    cart_serialize = []
                    cs={}
                    for cart in scart.carts.all():
                        price = cart.product.main_price - (cart.product.main_price * cart.product.discount / 100)
                        cost = price*cart.quantity
                        total_cost += cost
                        subtotal = total_cost
                        cs = {
                            "id": cart.id,
                            "category": cart.product.category.name,
                            "title": cart.product.title,
                            "image": cart.product.image,
                            "main_price": str(cart.product.main_price),
                            "price": str(cart.product.main_price - (cart.product.main_price * cart.product.discount / 100)),
                            "discount": str(cart.product.discount),
                            "amount": cart.quantity
                        }
                        cart_serialize.append(cs)
                    if scart.coupon.all().count() > 0:
                        cpn_dis = 0
                        for cpn in scart.coupon.all():
                            cpn_dis += cpn.value if cpn.discount_type.lower() == 'fixed' else total_cost * cpn.value / 100
                        total_cost -= cpn_dis
                    item = scart.carts.all().count()
                    msg = "Product successfully added to cart!"
                    context = {
                        'item':item,
                        'cost':total_cost,
                        'subtotal': subtotal,
                        'msg': msg,
                        'product': pro,
                        'cart': cart_serialize
                    }
                    return JsonResponse(context)
            else:
                return JsonResponse({'msg': "Product is not exist."})

def CartView(request):
    if request.method == 'POST':
        getcart = Cart.objects.get(id = request.POST['cart-id'])
        if getcart.product.amount < int(request.POST["quantity"]):
            msg = f"We have only {getcart.product.amount} product"
            msg_type = 'quantity-update-fail'
            messages.error(request, msg, extra_tags=msg_type)
            return redirect(request.path_info)
        else:
            getcart.quantity = request.POST["quantity"]
            getcart.save()
            return redirect(request.path_info)

    else:
        categorys = Category.objects.all()
        local_shipping = ShippingMethod.objects.filter(method_type = 'local').first()
        free_shipping = ShippingMethod.objects.filter(method_type = 'free').first()
        scart = ShopCart.objects.get(user = request.user, on_order=False)
        total_cost = 0
        subtotal = 0
        for cart in scart.carts.all():
            price = cart.product.main_price - (cart.product.main_price * cart.product.discount / 100)
            cost = price*cart.quantity
            total_cost += cost
            subtotal = total_cost
        if scart.coupon.all().count() > 0:
                cpn_dis = 0
                for cpn in scart.coupon.all():
                    cpn_dis += cpn.value if cpn.discount_type.lower() == 'fixed' else total_cost * cpn.value / 100
                total_cost -= cpn_dis
        item = scart.carts.all().count()
        context = {
            'category': categorys,
            'shopcart': scart,
            'subtotal': subtotal,
            'cost': total_cost,
            'local_shipping': local_shipping,
            'free_shipping': free_shipping,
            'item': item
        }
        return render(request, 'product/cart.html', context)

def CartDelete(request):
    getcart = Cart.objects.get(id = request.POST['id'])
    getcart.delete()
    scart = ShopCart.objects.get(user = request.user, on_order=False)
    total_cost = 0
    subtotal = 0
    cart_serialize = []
    cs={}
    for cart in scart.carts.all():
        price = cart.product.main_price - (cart.product.main_price * cart.product.discount / 100)
        cost = price*cart.quantity
        total_cost += cost
        subtotal = total_cost
        cs = {
            "id": cart.id,
            "category": cart.product.category.name,
            "title": cart.product.title,
            "image": cart.product.image,
            "main_price": str(cart.product.main_price),
            "price": str(cart.product.main_price - (cart.product.main_price * cart.product.discount / 100)),
            "discount": str(cart.product.discount),
            "amount": cart.quantity
        }
        cart_serialize.append(cs)
    if scart.coupon.all().count() > 0:
            cpn_dis = 0
            for cpn in scart.coupon.all():
                cpn_dis += cpn.value if cpn.discount_type.lower() == 'fixed' else total_cost * cpn.value / 100
            total_cost -= cpn_dis
    item = scart.carts.all().count()
    msg = "Product successfully deleted"
    context = {
        'item':item,
        'cost':total_cost,
        'subtotal': subtotal,
        'msg': msg,
        'cart': cart_serialize
    }
    return JsonResponse(context)

def Checkout(request):
    if request.method == 'POST':
        if 'coupon-code' in request.POST:
            if Coupon.objects.filter(code = request.POST['coupon-code']).exists():
                cpn = Coupon.objects.get(code = request.POST['coupon-code'])
                if request.COOKIES['cart'] == 'ucart':
                    scart = ShopCart.objects.get(user = request.user, on_order=False)
                else:
                    scart = ShopCart.objects.get(device = request.COOKIES['device'], on_order=False)
                cost = 0
                total_cost = 0
                for cart in scart.carts.all():
                    price = cart.product.main_price - (cart.product.main_price * cart.product.discount / 100)
                    cost = price*cart.quantity
                    total_cost += cost
                if scart.coupon.all().count() > 0:
                    for coupon in cart.coupon.all():
                        if coupon.discount_type == 'Percent':
                            total_cost_with_coupon = total_cost - total_cost*coupon.value/100
                        else:
                            total_cost_with_coupon = total_cost - coupon.value
                    total_cost = total_cost_with_coupon
                    
                cpn_used = ShopCart.objects.filter(coupon=cpn).count()
                currency = Currency.objects.get(code = request.COOKIES['mycurrency'])
                if request.COOKIES['cart'] == 'ucart':
                    my_used = ShopCart.objects.filter(user = request.user, coupon = cpn).count()
                else:
                    my_used = ShopCart.objects.filter(device = request.COOKIES['device'], coupon = cpn).count()
                if cpn.limit_per_coupon != None and cpn_used >= cpn.limit_per_coupon:
                    messages.error(request, 'This coupon have used maximum number of times..', extra_tags='cpn-error')
                elif cpn.limit_per_customer != None and my_used >= cpn.limit_per_customer:
                    messages.error(request, 'You have used this coupon maximum number of times.', extra_tags='cpn-error')
                elif cpn.max_spend != None and total_cost >= cpn.max_spend:
                    messages.error(request, f'This coupon is valid for maximum {currency.symbol_native}{cpn.max_spend*currency.rate}.', extra_tags='cpn-error')
                elif cpn.min_spend != None and total_cost <= cpn.min_spend:
                    messages.error(request, f'This coupon is valid for minimum {currency.symbol_native}{cpn.max_spend*currency.rate}.', extra_tags='cpn-error')
                else:
                    scart.coupon.add(cpn)
                    return redirect(request.path_info)
                return redirect(request.path_info)
            else:
                messages.error(request, 'Invalid coupon code.', extra_tags='cpn-error')
                return redirect(request.path_info)
        else:
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

            company_name = request.POST['company_name']
            payment_mode = 'cash'
            email = request.POST['email']
            notes = request.POST['notes']
            phone = request.POST['phone']
            rate = request.POST['rate']
            total = 0
            total_bdt = 0
            shipping_fee = 0 if float(total_bdt) >= ShippingMethod.objects.get(method_type = 'free').fee else ShippingMethod.objects.get(method_type = 'local').fee
            ordr = Order(
                user = usr,
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
            total = 0
            for cart in get_shopcart:
                cart.order_id = ordr.id
                cart.on_order = True
                cart.save()
                total += (cart.product.main_price - (cart.product.main_price * cart.product.discount / 100)) * cart.quantity
                ids = cart.product.id
                get_pro = Product.objects.get(id = ids)
                qntity = get_pro.amount - int(cart.quantity)
                if qntity < 0:
                    qntity = 0
                get_pro.amount = qntity
                get_pro.save()
                ordr.shopcarts.add(cart)
                ordr.save()
            ordr.total_bdt = total - int(ordr.shipping_fee)
            ordr.total = total * float(rate)
            ordr.save()
            countrys = Country.objects.all()
            address_book = AddressBook.objects.filter(user = request.user)
            context = {
                'address_book': address_book,
                'countrys': countrys
            }
            return render(request, 'account/profile.html', context)
    else:
        # import requests
        # urls = "https://fcsapi.com/api-v2/forex/converter?symbol=BDT/USD&amount=1&access_key=ohHkx8n2tCX9BBoaGvFUwY"
        # resp = requests.get(urls)
        # print("1 ----------> ", resp.json())
        category = Category.objects.all()
        countrys = Country.objects.all()
        scart = ShopCart.objects.get(user = request.user, on_order=False)
        total_cost = 0
        subtotal = 0
        for cart in scart.carts.all():
            price = cart.product.main_price - (cart.product.main_price * cart.product.discount / 100)
            cost = price*cart.quantity
            total_cost += cost
            subtotal = total_cost
        if scart.coupon.all().count() > 0:
            cpn_dis = 0
            for cpn in scart.coupon.all():
                cpn_dis += cpn.value if cpn.discount_type.lower() == 'fixed' else total_cost * cpn.value / 100
            total_cost -= cpn_dis
        item = scart.carts.all().count()
        local_shipping = ShippingMethod.objects.filter(method_type = 'local').first()
        free_shipping = ShippingMethod.objects.filter(method_type = 'free').first()
        paypal = PaymentMethod.objects.filter(name='paypal').first()
        context = {
            'category': category,
            'countrys': countrys,
            'local_shipping': local_shipping,
            'free_shipping': free_shipping,
            'paypal': paypal,
            'shopcart': scart,
            'cost': total_cost,
            'subtotal': subtotal,
            'item': item

        }
        return render(request, 'product/checkout.html', context)

def AddtoWishlist(request):
    if Wishlist.objects.filter(product__id = request.POST['id'], user = request.user).exists():
        Wishlist.objects.get(product__id = request.POST['id'], user = request.user).delete()
        context = {
            'type': 'fail',
            'msg': 'Product successfully removed from wishlist.'
        }
        return JsonResponse(context)
    wishlist = Wishlist(
        user = request.user,
        product = Product.objects.get(id = request.POST['id'])
    )
    wishlist.save()
    return JsonResponse({'type': 'success', 'msg': 'Product successfully added to wishlist.'})

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