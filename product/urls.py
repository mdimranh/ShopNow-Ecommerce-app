from django.urls import path
from .views import ProductDetails, CategoryProduct

urlpatterns = [
    path('products/<int:id>', ProductDetails, name='productdetails'),
    path('category/<int:id>/<slug:slug>', CategoryProduct, name='category_product'),
]
