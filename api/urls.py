
from django.urls import path
from .views import *

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("products", Products),
    path("product/<int:id>", ProductDetail),
    path("categories", Categories),
    path("category/<int:id>", CategoryDetails),
    path("login", obtain_auth_token),
    path("registration", RegistrationApi),
    path("users", UserDetails.as_view()),
    path("token", TokenObtainPairView.as_view()),
    path("token/refresh", TokenRefreshView.as_view()),
    path("tokenapi", tokenApi.as_view()),
    path("shopcart", MyShopcart),
    path("wishlist", MyWishlist),
    path("wishlist/delete/<int:id>", DeleteWishlist),
    path("shopcart/add", AddddToCart),

]
