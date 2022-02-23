from django.urls import path
from .views import Dashboard, Menu, Login, Users, UserDetails
from .product import Products, EditProduct, CategoryView, ImagesSave, deleteProduct, CategoryDelete, GroupDelete, SubcategoryDelete
from .coupon import CouponView, CouponDetails
from .settings import SettingView

urlpatterns = [
    path("", Dashboard, name="admin-dashboard"),
    path("product/", Products, name="admin-products"),
    path("product/imagesave/", ImagesSave, name="admin-products-image-save"),
    path("product/edit-product/<int:id>", EditProduct, name="admin-edit-product"),
    path("product/delete-product/", deleteProduct, name="admin-delete-product"),
    path("category", CategoryView),
    path("coupon", CouponView),
    path("coupon/<int:id>", CouponDetails),
    path("menu", Menu),
    path("login", Login, name = "admin-login"),
    path("user", Users, name = "admin-users"),
    path("user/<int:id>", UserDetails, name = "admin-users-details"),
    path("settings/", SettingView, name="admin-settings"),
    path("category/delete/<int:id>", CategoryDelete, name="admin-category-delete"),
    path("group/delete/<int:id>", GroupDelete, name="admin-group-delete"),
    path("subcategory/delete/<int:id>", SubcategoryDelete, name="admin-subcategory-delete"),
    path("settings/", SettingView, name="admin-settings"),
    path("settings/", SettingView, name="admin-settings"),
]
