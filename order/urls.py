from django.urls import path
from .views import AddToCart, CartView, CartDelete, Checkout, WishList, AddtoWishlist, WishItemDelete, PlaceOrder

urlpatterns = [
    # path('ajax/addtocart', AddtoCart, name='addtocart'),
    path('ajax/addtocart', AddToCart.as_view(), name='addtocart'),
    path('cart', CartView, name='cartview'),
    path('wishlist', WishList, name='wishlist'),
    path('ajax/addtowishlist', AddtoWishlist, name='addtowishlist'),
    path('ajax/deletewishlist', WishItemDelete, name='deletewishlist'),
    path('cart/checkout', Checkout, name='checkout'),
    path('ajax/cartdelete', CartDelete, name='cartdelete'),
    path('place-order', PlaceOrder, name='placeorder'),
]
