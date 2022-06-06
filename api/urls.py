
from django.urls import path, re_path
from .views import *

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    re_path(r'^products$', Products.as_view()),
    path("product/<int:id>", ProductDetails.as_view()),
    path("categories", Categories.as_view()),
    path("category/<int:id>", CategoryDetails.as_view()),
    path("login", obtain_auth_token),
    path("registration", Registration.as_view()),
    path("user/<int:id>", UserDetails.as_view()),
    path("token", TokenObtainPairView.as_view()),
    path("token/refresh", TokenRefreshView.as_view()),
    path("tokenapi", tokenApi.as_view()),
    path("myshopcart", MyShopcart),
    path("wishlist", MyWishlist),
    path("wishlist/delete/<int:id>", DeleteWishlist),
    path("cart/add", AddddToCart),
    path("addressbook/<int:id>", AddressBookDetails.as_view()),
    path("totalcartcost/<int:id>", TotalCartCost.as_view()),
    path("review", AddReview.as_view()),
    re_path(r"^products/(?P<data_type>.+)$", complexProducts),
]
