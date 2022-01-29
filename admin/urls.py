from django.urls import path
from .views import *
from .product import Products, EditProduct

urlpatterns = [
    path("control/", Dashboard),
    path("control/product", Products),
    path("control/product/edit-product/<int:id>", EditProduct)
]
