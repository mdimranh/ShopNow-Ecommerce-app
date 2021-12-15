from django.urls import path
from .views import AddtoCart, CartView

urlpatterns = [
    path('ajax/addtocart', AddtoCart, name='addtocart'),
    # path('ajax/getcart', GetCart, name='getcart'),
    path('cart', CartView, name='cartview'),
]
