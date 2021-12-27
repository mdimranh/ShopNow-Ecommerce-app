from django.urls import path
from .views import AddtoCart, CartView, CartDelete, Checkout, WishList, AddtoWishlist

urlpatterns = [
    path('ajax/addtocart', AddtoCart, name='addtocart'),
    path('cart', CartView, name='cartview'),
    path('wishlist', WishList, name='wishlist'),
    path('ajax/addtowishlist', AddtoWishlist, name='addtowishlist'),
    path('cart/checkout', Checkout, name='checkout'),
    path('ajax/cartdelete', CartDelete, name='cartdelete'),
]
