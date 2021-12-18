from django.urls import path
from .views import AddtoCart, CartView, CartDelete, Checkout

urlpatterns = [
    path('ajax/addtocart', AddtoCart, name='addtocart'),
    # path('ajax/getcart', GetCart, name='getcart'),
    path('cart', CartView, name='cartview'),
    path('cart/checkout', Checkout, name='checkout'),
    path('cartdelete/<int:id>', CartDelete, name='cartdelete'),
]
