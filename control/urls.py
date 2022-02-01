from django.urls import path
from .views import Dashboard, Menu, Login
from .product import Products, EditProduct, CategoryView
from .coupon import CouponView, CouponDetails

urlpatterns = [
    path("control/", Dashboard, name="admin-dashboard"),
    path("control/product/", Products, name="admin-products"),
    path("control/product/edit-product/<int:id>", EditProduct, name="admin-edit-product"),
    path("control/category", CategoryView),
    path("control/coupon", CouponView),
    path("control/coupon/<int:id>", CouponDetails),
    path("control/menu", Menu),
    path("control/login", Login, name = "admin-login"),
]
