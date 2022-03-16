from django.shortcuts import render
from django.http import JsonResponse
from order.models import Order

from django.views import View
from django.views.generic import ListView

class OrderList(View):
    def get(self, request):
        orders = Order.objects.all()
        context = {
            'orders': orders,
            'sales_sec': True,
            'orders_sec': True
        }
        return render(request, "control/order.html", context)

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
        get_order.status = request.POST['status']
        get_order.save()
        context = {
            'msg': "success"
        }
        return JsonResponse(context)