from django.shortcuts import render
from django.http import JsonResponse
from order.models import Order

from django.views import View
from django.views.generic import ListView, TemplateView
from order.models import ShopCart
from product.models import Product

from django.utils import timezone

# class OrderList(View):
#     def get(self, request):
#         orders = Order.objects.all()
#         context = {
#             'orders': orders,
#             'sales_sec': True,
#             'orders_sec': True
#         }
#         return render(request, "control/order.html", context)

class OrderList(TemplateView):
    template_name = 'control/order.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.all()
        context['sales_sec'] = True
        context['orders_sec'] = True
        return context

class OrderDetails(View):
    def get(self, request, id):
        get_order = Order.objects.get(id = id)
        context = {
            'order': get_order,
            'sales_sec': True,
            'orders_sec': True
        }
        return render(request, "control/order.html", context)

    def post(self, request, id):
        get_order = Order.objects.get(id = id)
        if request.POST['status'] == 'canceled':
            get_shopcart = ShopCart.objects.filter(user = request.user, order_id = get_order.id)
            for cart in get_shopcart:
                ids = cart.product.id
                get_pro = Product.objects.get(id = ids)
                qntity = get_pro.amount + int(cart.quantity)
                get_pro.amount = qntity
                get_pro.save()
        else:
            if get_order.status == 'canceled':
                get_shopcart = ShopCart.objects.filter(user = request.user, order_id = get_order.id)
                for cart in get_shopcart:
                    ids = cart.product.id
                    get_pro = Product.objects.get(id = ids)
                    qntity = get_pro.amount - int(cart.quantity)
                    get_pro.amount = qntity
                    get_pro.save()
        get_order.status = request.POST['status']
        get_order.update = timezone.now()
        get_order.save()
        context = {
            'msg': "success"
        }
        return JsonResponse(context)