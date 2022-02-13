from django.urls import path
from .views import Dashboard, Menu, Login, Users, UserDetails
from .product import Products, EditProduct, CategoryView
from .coupon import CouponView, CouponDetails
from .settings import SettingView

urlpatterns = [
    path("", Dashboard, name="admin-dashboard"),
    path("product/", Products, name="admin-products"),
    path("product/edit-product/<int:id>", EditProduct, name="admin-edit-product"),
    path("category", CategoryView),
    path("coupon", CouponView),
    path("coupon/<int:id>", CouponDetails),
    path("menu", Menu),
    path("login", Login, name = "admin-login"),
    path("user", Users, name = "admin-users"),
    path("user/<int:id>", UserDetails, name = "admin-users-details"),
    path("settings/", SettingView, name="admin-settings"),
]
