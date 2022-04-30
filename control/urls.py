from django.urls import path
from .views import *
from .product import *
from .coupon import CouponView, CouponDetails, DeleteCoupon
from .settings import *
from .newsletter import NewsletterList, AddNewsletter, NewsletterDetails
from .orders import OrderList, OrderDetails

from django.views.generic import TemplateView

urlpatterns = [
    path("", Dashboard, name="admin-dashboard"),
    path("/product", Products, name="admin-products"),
    path("/product/imagesave", ImagesSave, name="admin-products-image-save"),
    path("/product/deleteimage", deleteImage),
    path("/product/edit-product/<int:id>", EditProduct.as_view(), name="admin-edit-product"),
    path("/product/delete-product", deleteProduct, name="admin-delete-product"),
    path("/category", CategoryView),
    path("/brand", BrandView.as_view()),
    path("/brand/<int:id>", BrandDetails.as_view()),
    path("/brand/delete", deleteBrand),
    path("/coupon", CouponView.as_view()),
    path("/coupon/<int:id>", CouponDetails.as_view()),
    path("/coupon/delete-coupon", DeleteCoupon.as_view()),
    path("/menu", Menu),
    path("/menu/update", MenuUpdate),
    path("/message", Message),
    path("/message/<int:id>", MessageDetails),
    path("/pages", PageList),
    path("/pages/<int:id>", PageDetails),
    path("/page/delete-page", DeletePage.as_view()),
    path("/login", Login, name = "admin-login"),
    path("/user", Users.as_view(), name = "admin-users"),
    path("/user/<int:id>", UserDetails.as_view(), name = "admin-users-details"),
    path("/role", Roles.as_view(), name = "admin-users-role"),
    path("/role/<int:id>", RoleDetails.as_view(), name = "admin-users-role-details"),
    path("/settings", SettingView, name="admin-settings"),
    path("/category/delete/<int:id>", CategoryDelete, name="admin-category-delete"),
    path("/group/delete/<int:id>", GroupDelete, name="admin-group-delete"),
    path("/subcategory/delete/<int:id>", SubcategoryDelete, name="admin-subcategory-delete"),
    path("/settings", SettingView, name="admin-settings"),
    path("/slider", Sliders, name="admin-sliders"),
    path("/slider/<int:id>", SliderDetails, name="admin-slider-details"),
    path("/banners", Banners.as_view(), name="admin-banners"),
    path("/banner/<int:id>", BannerDetails.as_view(), name="admin-banner-details"),
    path("/sitefront", SiteFrontView, name="admin-sitefront"),
    path("/carousel/update", CarouselUpdate.as_view(), name="admin-carousel-update"),
    path("/area", Area.as_view(), name="admin-area"),
    path("/area/delete", Area.as_view(), name="admin-area-delete"),
    path("/currency", CurrencyList.as_view(), name="admin-currency"),
    path("/currency/<int:id>", CurrencyView.as_view(), name="admin-currency-view"),
    path("/orders", OrderList.as_view(), name="admin-orders"),
    path("/order/<int:id>", OrderDetails.as_view(), name="admin-rrdersetails"),
    path("/newsletter", NewsletterList.as_view(), name="admin-newsletterlist"),
    path("/addnewsletter", AddNewsletter.as_view(), name="admin-addnewsletter"),
    path("/newsletter/<int:id>", NewsletterDetails.as_view(), name="admin-newsletter-details"),
]
