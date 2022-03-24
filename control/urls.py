from django.urls import path
from .views import *
from .product import *
from .coupon import CouponView, CouponDetails, DeleteCoupon
from .settings import SettingView, Sliders, SliderDetails, SiteFrontView, PageList, PageDetails, DeletePage
from .orders import OrderList, OrderDetails

from django.views.generic import TemplateView

urlpatterns = [
    path("", Dashboard, name="admin-dashboard"),
    path("product/", Products, name="admin-products"),
    path("product/imagesave/", ImagesSave, name="admin-products-image-save"),
    path("product/edit-product/<int:id>", EditProduct, name="admin-edit-product"),
    path("product/delete-product/", deleteProduct, name="admin-delete-product"),
    path("category", CategoryView),
    path("coupon", CouponView.as_view()),
    path("coupon/<int:id>", CouponDetails),
    path("coupon/delete-coupon", DeleteCoupon.as_view()),
    path("menu", Menu),
    path("menu/update", MenuUpdate),
    path("message", Message),
    path("message/<int:id>", MessageDetails),
    path("pages", PageList),
    path("pages/<int:id>", PageDetails),
    path("page/delete-page", DeletePage.as_view()),
    path("login", Login, name = "admin-login"),
    path("user", Users.as_view(), name = "admin-users"),
    path("user/<int:id>", UserDetails.as_view(), name = "admin-users-details"),
    path("role", Roles.as_view(), name = "admin-users-role"),
    path("role/<int:id>", RoleDetails.as_view(), name = "admin-users-role-details"),
    path("settings/", SettingView, name="admin-settings"),
    path("category/delete/<int:id>", CategoryDelete, name="admin-category-delete"),
    path("group/delete/<int:id>", GroupDelete, name="admin-group-delete"),
    path("subcategory/delete/<int:id>", SubcategoryDelete, name="admin-subcategory-delete"),
    path("settings/", SettingView, name="admin-settings"),
    path("slider/", Sliders, name="admin-sliders"),
    path("slider/<int:id>", SliderDetails, name="admin-slider-details"),
    path("sitefront", SiteFrontView, name="admin-sitefront"),
    # path("sitefront/<int:id>", SliderDetails, name="admin-sitefront"),
    path("orders", OrderList.as_view(), name="admin-orders"),
    path("order/<int:id>", OrderDetails.as_view(), name="admin-rrdersetails"),
]
