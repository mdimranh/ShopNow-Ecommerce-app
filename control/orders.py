from django.shortcuts import render
from django.http import JsonResponse
from order.models import Order

from order.cartdetails import cartDetails

from django.views import View
from django.views.generic import ListView, TemplateView
from order.models import ShopCart
from product.models import Product

from django.utils import timezone

from setting.models import Settings
from setting.models import EmailConfig
from django.template.loader import render_to_string
from setting.models import Currency, SiteConfiguration
from django.core.mail import EmailMultiAlternatives
from control.emailconfig import backend
from django.contrib.sites.shortcuts import get_current_site

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
            for cart in get_order.shopcart.carts.all():
                ids = cart.product.id
                get_pro = Product.objects.get(id = ids)
                qntity = get_pro.amount + int(cart.quantity)
                get_pro.amount = qntity
                get_pro.save()
        else:
            if get_order.status == 'canceled':
                for cart in get_order.shopcart.carts.all():
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
        try:
            return JsonResponse(context)
        finally:
            if request.POST['status'] == 'completed':
                mail_config = EmailConfig.objects.get()
                subject, from_email, to = 'Confirm delivered', mail_config.email_host_user, get_order.email
                text_content = 'Confirm delivered'
                html_content = render_to_string('order-delivard.html', context={
                    'order': get_order,
                    'currency': Settings.objects.get().default_currency,
                    'domain': get_current_site(request).domain
                })
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to], connection=backend)
                msg.attach_alternative(html_content, "text/html")
                msg.send()