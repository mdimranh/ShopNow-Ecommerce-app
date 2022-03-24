from django.views import View
from django.shortcuts import render, redirect
from django.http import JsonResponse
from product.models import Product, Category
from order.models import Coupon

class CouponView(View):
    def get(self, request):
        products = Product.objects.all()
        categorys = Category.objects.all()
        coupons = Coupon.objects.all()
        context = {
            "products": products,
            "categories": categorys,
            "coupons": coupons
        }
        return render(request, "control/coupon.html", context)
    def post(self, request):
        free_ship = True if request.POST.get('free-shipping') == 'on' else False
        active = True if request.POST.get('active') == 'on' else False
        if len(request.POST['min-spend']) > 0:
            min_spend = request.POST['min-spend']
        else:
            min_spend = 0
        if len(request.POST['max-spend']) > 0:
            max_spend = request.POST['max-spend']
        else:
            max_spend = 0
        if len(request.POST['limit-per-coupon']) > 0:
            limit_per_coupon = request.POST['limit-per-coupon']
        else:
            limit_per_coupon = 0
        if len(request.POST['limit-per-customer']) > 0:
            limit_per_customer = request.POST['limit-per-customer']
        else:
            limit_per_customer = 0
        cpn = Coupon(
            name=request.POST['name'],
            code=request.POST['code'],
            discount_type=request.POST['discount-type'],
            value=request.POST['quantity'],
            free_shipping=free_ship,
            start_date=request.POST['start-date'],
            end_date=request.POST['end-date'],
            min_spend=min_spend,
            max_spend=max_spend,
            limit_per_coupon=limit_per_coupon,
            limit_per_customer=limit_per_customer,
            active=active
        )
        cpn.save()
        for pro in request.POST.getlist('products'):
            cpn.products.add(pro)
            cpn.save()
        for pro in request.POST.getlist('exclude-products'):
            cpn.exclude_products.add(pro)
            cpn.save()
        for cat in request.POST.getlist('categories'):
            cpn.categories.add(cat)
            cpn.save()
        for cat in request.POST.getlist('exclude-categories'):
            cpn.exclude_categories.add(cat)
            cpn.save()
        
        return redirect(request.path_info)

def CouponDetails(request, id):
    cpn = Coupon.objects.get(id = id)
    products = Product.objects.all()
    categorys = Category.objects.all()
    context = {
        "products": products,
        "categorys": categorys,
        "coupon": cpn
    }
    return render(request, "control/edit-coupon.html", context)

class DeleteCoupon(View):
    def post(self, request):
        total_coupon = len(request.POST["coupons"].split(','))
        for coupon_id in request.POST["coupons"].split(','):
            Coupon.objects.get(id = coupon_id).delete()
        context = {
            'total' : total_coupon
        }
        return JsonResponse(context)